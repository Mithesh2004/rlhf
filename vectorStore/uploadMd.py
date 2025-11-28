from pathlib import Path
import uuid
from typing import List, Tuple

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
import re

def split_markdown_by_individual_headers(text: str, headers_to_split_on):
    """
    Splits markdown so each header (h1-h6) and its *own* content 
    form a separate Document, without including nested sections.
    """
    # Create regex pattern from headers list
    header_pattern = "|".join(
        [rf"(?P<{tag}>{re.escape(header)} .*)" for header, tag in headers_to_split_on]
    )
    regex = re.compile(f"({header_pattern})")

    # Find all header matches
    matches = list(regex.finditer(text))
    docs = []

    for i, match in enumerate(matches):
        header_text = match.group(0)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        # Identify header type (h1, h2, etc.)
        header_type = [t for h, t in headers_to_split_on if match.group(t)]
        header_type = header_type[0] if header_type else "unknown"

        docs.append(
            Document(
                page_content=f"{header_text}\n{content}",
                metadata={"header_type": header_type, "header": header_text.strip("# ").strip()},
            )
        )
    return docs

def split_markdown_by_h2_only(text: str,disease_name:str,department:str):
    """
    Splits markdown so that each chunk corresponds to a '##' (h2) section.
    Extracts document-level metadata: ICD codes, disease name, and version.
    """
    # Extract document-level metadata
    version_match = re.search(r'^([A-Za-z]+/\d{4})', text, re.MULTILINE)
    version = version_match.group(1) if version_match else None
    
    # Extract ICD codes
    icd_match = re.search(r'ICD-10-([^\n]+)', text)
    icd_code = f"ICD-10-{icd_match.group(1).strip()}" if icd_match else None
    
    # Regex: matches lines starting with exactly '##' but not '###'
    regex = re.compile(r"(^## [^\n]+)", re.MULTILINE)
    matches = list(regex.finditer(text))
    docs = []

    for i, match in enumerate(matches):
        header_text = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        docs.append(
            Document(
                page_content=f"{header_text}\n{content}",
                metadata={
                    "header_type": "h2",
                    "header": header_text.strip("# ").strip(),
                    "disease": disease_name,
                    "icd_code": icd_code,
                    "version": version,
                    "department":department,
                },
            )
        )

    # If no ## found, treat whole doc as one chunk
    if not docs:
        docs = [
            Document(
                page_content=text.strip(),
                metadata={
                    "header_type": "none",
                    "disease": disease_name,
                    "icd_code": icd_code,
                    "version": version,
                    "department":department,
                }
            )
        ]
        print(docs[-1])
    return docs


# -------- Settings --------
FOLDER_PATH = "output"
COLLECTION_NAME = "icmr_data"
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384  
BATCH_SIZE = 512

# Headers to track; adjust as needed
HEADERS_TO_SPLIT_ON: List[Tuple[str, str]] = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
    ("####", "h4"),
    ("#####", "h5"),
    ("######", "h6"),
]

# -------- Helpers --------
def get_all_md_in_folder(folder_path: str):
    folder = Path(folder_path)
    return list(folder.rglob("*.md"))

# -------- Load files --------
md_paths = get_all_md_in_folder(FOLDER_PATH)

# -------- Init clients --------
client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Create collection if it doesn't exist
try:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=EMBEDDING_DIM,
            distance=models.Distance.COSINE,
        ),
    )
except Exception:
    # Collection likely exists; proceed
    print(f"collection{COLLECTION_NAME} exists:)")
    pass

# -------- Splitter --------
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=HEADERS_TO_SPLIT_ON,
    strip_headers=True,   # set False to keep headers in chunk text
    # return_each_line=False (default)
)

# -------- Build points --------
points: List[models.PointStruct] = []

for md_path in md_paths:
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    # docs = markdown_splitter.split_text(text)  # returns list of LangChain Document objects
    # docs = split_markdown_by_individual_headers(text, HEADERS_TO_SPLIT_ON)
    
    docs = split_markdown_by_h2_only(text,md_path.stem,md_path.parent.name)

    for idx, doc in enumerate(docs):
        content = (doc.page_content or "").strip()
        if not content:
            continue

        # Embed the chunk
        embedding = model.encode(content, normalize_embeddings=True).tolist()
        # embedding = model.encode(content).tolist()

        # Compose payload including header metadata and provenance
        payload = {
            "file_path": str(md_path),
            "chunk_index": idx,
            "headers": doc.metadata,  # hierarchical header mapping, e.g., {"h1": "...", "h2": "..."}
            "text": content,
        }

        points.append(
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=payload,
            )
        )

# -------- Upsert in batches --------
for i in range(0, len(points), BATCH_SIZE):
    batch = points[i : i + BATCH_SIZE]
    client.upsert(collection_name=COLLECTION_NAME, points=batch)

print(f"Indexed {len(points)} chunks from {len(md_paths)} markdown files into '{COLLECTION_NAME}'.")
