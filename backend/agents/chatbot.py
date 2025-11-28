import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Set, Literal
from dotenv import load_dotenv
from pydantic import BaseModel

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class ResponseType(BaseModel):
    """Structured response from the chatbot"""
    type: Literal["question", "diagnosis"]
    content: str
    reasoning: Optional[str] = None


class ICMRDiagnosticChatbot:
    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "icmr_data",
        embedding_model: str = "BAAI/bge-small-en-v1.5",
        gemini_model: str = "gemini-2.5-flash",
        top_k: int = 10,
        min_questions: int = 5,
        max_questions: int = 10,
        confidence_threshold: float = 0.85
    ):
        """Initialize the diagnostic chatbot with Qdrant and Gemini"""
        logger.info("Initializing ICMR Diagnostic Chatbot...")
        
        # Store configuration
        self.min_questions = min_questions
        self.max_questions = max_questions
        self.confidence_threshold = confidence_threshold
        
        # Initialize Qdrant client
        try:
            self.client = QdrantClient(url=qdrant_url)
            self.collection_name = collection_name
            collections = self.client.get_collections()
            logger.info(f"✅ Connected to Qdrant at {qdrant_url}")
            
            collection_names = [col.name for col in collections.collections]
            if collection_name not in collection_names:
                logger.warning(f"⚠️  Collection '{collection_name}' not found. Available: {collection_names}")
            else:
                logger.info(f"✅ Collection '{collection_name}' found")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Qdrant: {e}")
            raise ConnectionError(f"Qdrant connection failed: {e}")
        
        # Initialize embedding model
        try:
            self.encoder = SentenceTransformer(embedding_model)
            logger.info(f"✅ Loaded embedding model: {embedding_model}")
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {e}")
            raise
        
        # Initialize Gemini
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            logger.error("❌ GOOGLE_API_KEY not found in environment variables")
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=gemini_model,
                google_api_key=google_api_key,
                temperature=0.3,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
            logger.info(f"✅ Initialized Gemini model: {gemini_model}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {e}")
            raise
        
        self.top_k = top_k
        
        # Session storage
        self.store = {}
        self.current_session_id = "default_session"
        self.session_states = {}
        self._init_session_state(self.current_session_id)
        
        # Build chains
        self._build_chains()
        
        logger.info("✅ Chatbot initialization complete")
    
    def _init_session_state(self, session_id: str):
        """Initialize state for a new session"""
        self.session_states[session_id] = {
            "initial_symptoms": [],
            "asked_questions": [],
            "asked_categories": set(),
            "potential_diseases": [],
            "question_count": 0,
            "current_context": [],
            "aspects_covered": set(),
            "disease_evidence": {},
            "is_concluded": False
        }
        logger.debug(f"Initialized session state for: {session_id}")
    
    def get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """Get or create chat history for a session"""
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]
    
    def _build_chains(self):
        """Build LangChain chains with message history"""
        
        # Question generation chain with structured output
        self.question_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert medical diagnostician using ICMR clinical guidelines. Your role is to ask ONE targeted question OR provide a final diagnosis.

**CURRENT SITUATION:**
- Question {question_count}/{max_questions} (Minimum: {min_questions})
- Aspects covered: {aspects_covered}
- Top candidates from ICMR data: {candidates}

**DECISION CRITERIA:**

Generate a **QUESTION** if:
- Question count < {min_questions}, OR
- Important aspects still unexplored: {uncovered_aspects}, OR
- Top candidate confidence < {confidence_threshold}%

Generate a **DIAGNOSIS** if:
- Question count >= {min_questions} AND
- At least 4 aspects covered AND
- Top candidate confidence >= {confidence_threshold}% OR
- Question count >= {max_questions} (MUST diagnose)

**QUESTION GUIDELINES** (if asking):
Focus on: {current_category}
- Use SPECIFIC medical terminology from ICMR data
- Reference the candidate diseases: {candidates}
- Ask about aspects NOT covered: {uncovered_aspects}
- Keep under 25 words
- Be clinically precise

**RELEVANT ICMR CLINICAL DATA:**
{context}

**PREVIOUS QUESTIONS ASKED:**
{asked_questions}

**OUTPUT FORMAT:**
You MUST respond with ONLY a valid JSON object in this exact format:
{{
  "type": "question",
  "content": "Your specific medical question here",
  "reasoning": "Brief reason for asking this question"
}}

OR if providing diagnosis:
{{
  "type": "diagnosis",
  "content": "## Possible Conditions\\n[Full diagnosis with all sections]\\n## Recommended Actions\\n...\\n## Further Evaluation\\n...\\n## Department Referral\\n...\\n## Urgency Level\\n...",
  "reasoning": "Sufficient information gathered"
}}

**CRITICAL**: Your response must be ONLY the JSON object, nothing else."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "Based on the patient's input and ICMR data, decide: ask a question OR provide diagnosis. Respond ONLY with JSON.")
        ])
        
        # Use JsonOutputParser for structured output
        self.question_chain = (
            self.question_prompt
            | self.llm
            | JsonOutputParser()
        )
        
        self.question_with_history = RunnableWithMessageHistory(
            self.question_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history"
        )
    
    def search_qdrant(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Search Qdrant for relevant medical information"""
        try:
            query_vector = self.encoder.encode(query, normalize_embeddings=True).tolist()
            
            search_params = {
                "collection_name": self.collection_name,
                "query_vector": query_vector,
                "limit": self.top_k,
                "with_payload": True,
                "score_threshold": 0.5
            }
            
            if filters:
                search_params["query_filter"] = filters
            
            results = self.client.search(**search_params)
            
            return [
                {
                    "text": hit.payload.get("text", ""),
                    "disease": hit.payload.get("disease", ""),
                    "department": hit.payload.get("department", ""),
                    "header": hit.payload.get("header", ""),
                    "icd_code": hit.payload.get("icd_code", ""),
                    "score": hit.score
                }
                for hit in results
            ]
        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            return []
    
    def get_state(self, session_id: Optional[str] = None) -> Dict:
        """Get current session state"""
        sid = session_id or self.current_session_id
        return self.session_states.get(sid, {})
    
    def determine_next_category(self, state: Dict) -> str:
        """Determine which aspect to ask about next"""
        priority_categories = [
            "temporal", "severity", "location", "character", 
            "associated", "modifying", "history"
        ]
        
        covered = state["aspects_covered"]
        for category in priority_categories:
            if category not in covered:
                return category
        
        return "differential"
    
    def calculate_confidence(self, disease_name: str, state: Dict) -> float:
        """Calculate confidence for a disease"""
        evidence = state["disease_evidence"].get(disease_name, {})
        base_score = evidence.get("avg_score", 0)
        match_count = evidence.get("match_count", 0)
        
        # Adjust confidence based on information gathered
        question_penalty = min(state["question_count"] / self.min_questions, 1.0)
        aspect_bonus = min(len(state["aspects_covered"]) / 5, 1.0)
        consistency_bonus = min(match_count / 4, 1.0)
        
        confidence = (
            base_score * 0.5 +
            question_penalty * 0.2 +
            aspect_bonus * 0.2 +
            consistency_bonus * 0.1
        )
        
        return confidence
    
    def analyze_symptoms(self, symptoms: str, session_id: str) -> Dict:
        """Analyze symptoms and retrieve potential diseases"""
        results = self.search_qdrant(symptoms)
        state = self.get_state(session_id)
        
        disease_scores = {}
        for result in results:
            disease = result["disease"]
            if disease:
                if disease not in disease_scores:
                    disease_scores[disease] = {
                        "scores": [],
                        "department": result["department"],
                        "icd_code": result["icd_code"],
                        "sections": set()
                    }
                disease_scores[disease]["scores"].append(result["score"])
                disease_scores[disease]["sections"].add(result["header"])
        
        for disease, data in disease_scores.items():
            avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
            state["disease_evidence"][disease] = {
                "avg_score": avg_score,
                "match_count": len(data["scores"]),
                "sections": list(data["sections"])
            }
            
            confidence = self.calculate_confidence(disease, state)
            disease_scores[disease].update({
                "score": avg_score,
                "confidence": confidence * 100,
                "match_count": len(data["scores"])
            })
        
        sorted_diseases = sorted(
            disease_scores.items(),
            key=lambda x: x[1]["confidence"],
            reverse=True
        )[:5]
        
        state["potential_diseases"] = [
            {"name": d[0], **d[1]} for d in sorted_diseases
        ]
        state["current_context"] = results
        
        return {"candidates": state["potential_diseases"], "context": results}
    
    def refine_diagnosis(self, new_info: str, session_id: str) -> None:
        """Refine potential diseases based on new information"""
        state = self.get_state(session_id)
        
        all_info = " ".join(state["initial_symptoms"]) + " " + new_info
        
        # Progressive filtering based on question count
        filters = None
        if state["question_count"] > 5 and state["potential_diseases"]:
            disease_names = [d["name"] for d in state["potential_diseases"][:3]]
            filters = {
                "should": [
                    {"key": "disease", "match": {"value": disease}}
                    for disease in disease_names
                ]
            }
        
        results = self.search_qdrant(all_info, filters)
        
        # Update disease evidence
        for result in results:
            disease = result["disease"]
            if disease:
                if disease in state["disease_evidence"]:
                    existing = state["disease_evidence"][disease]
                    existing["avg_score"] = (existing["avg_score"] + result["score"]) / 2
                    existing["match_count"] += 1
                else:
                    state["disease_evidence"][disease] = {
                        "avg_score": result["score"],
                        "match_count": 1,
                        "sections": [result["header"]]
                    }
        
        # Recalculate top diseases
        disease_confidences = {}
        for disease in state["disease_evidence"]:
            confidence = self.calculate_confidence(disease, state)
            disease_confidences[disease] = {
                "name": disease,
                "confidence": confidence * 100,
                "match_count": state["disease_evidence"][disease]["match_count"]
            }
        
        sorted_diseases = sorted(
            disease_confidences.items(),
            key=lambda x: x[1]["confidence"],
            reverse=True
        )[:3]
        
        state["potential_diseases"] = [d[1] for d in sorted_diseases]
        state["current_context"] = results
    
    def generate_response(self, session_id: str) -> Dict:
        """Generate next response (question or diagnosis)"""
        state = self.get_state(session_id)
        
        # Prepare context from ICMR data
        context_text = "\n\n".join([
            f"Disease: {doc['disease']}\n"
            f"Section: {doc['header']}\n"
            f"Content: {doc['text'][:400]}\n"
            f"Relevance: {doc['score']:.2f}"
            for doc in state["current_context"][:5]
        ])
        
        candidates = ", ".join([
            f"{d['name']} ({d.get('confidence', 0):.1f}%)"
            for d in state["potential_diseases"][:3]
        ])
        
        asked_questions = "\n".join(state["asked_questions"][-5:])
        
        all_aspects = {"temporal", "severity", "location", "character", "associated", "modifying", "history"}
        uncovered = all_aspects - state["aspects_covered"]
        uncovered_text = ", ".join(uncovered) if uncovered else "All aspects covered"
        
        current_category = self.determine_next_category(state)
        
        # Generate response with structured output
        try:
            response = self.question_with_history.invoke(
                {
                    "input": "generate next response",
                    "context": context_text if context_text else "No specific ICMR data retrieved yet.",
                    "candidates": candidates if candidates else "Analyzing initial symptoms...",
                    "asked_questions": asked_questions if asked_questions else "None",
                    "current_category": current_category,
                    "uncovered_aspects": uncovered_text,
                    "question_count": state["question_count"],
                    "max_questions": self.max_questions,
                    "min_questions": self.min_questions,
                    "aspects_covered": len(state["aspects_covered"]),
                    "confidence_threshold": int(self.confidence_threshold * 100)
                },
                config={"configurable": {"session_id": session_id}}
            )
            
            # Validate response structure
            if isinstance(response, dict) and "type" in response and "content" in response:
                return response
            else:
                # Fallback if JSON parsing fails
                logger.warning("Response not in expected format, falling back to question")
                return {
                    "type": "question",
                    "content": "Could you describe the symptoms in more detail?",
                    "reasoning": "Clarification needed"
                }
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "type": "question",
                "content": "Could you provide more details about your symptoms?",
                "reasoning": "Error in generation"
            }
    
    def chat(self, user_input: str, session_id: Optional[str] = None) -> Dict:
        """Main chat interface - returns structured response"""
        try:
            sid = session_id or self.current_session_id
            
            if sid not in self.session_states:
                self._init_session_state(sid)
            
            state = self.get_state(sid)
            history = self.get_session_history(sid)
            history.add_user_message(user_input)
            
            # First message: analyze symptoms
            if state["question_count"] == 0:
                state["initial_symptoms"].append(user_input)
                self.analyze_symptoms(user_input, sid)
            else:
                # Subsequent messages: refine diagnosis
                self.refine_diagnosis(user_input, sid)
            
            # Generate response
            response = self.generate_response(sid)
            
            # Update state based on response type
            if response["type"] == "question":
                state["question_count"] += 1
                state["asked_questions"].append(response["content"])
                category = self.determine_next_category(state)
                state["aspects_covered"].add(category)
            else:
                state["is_concluded"] = True
            
            history.add_ai_message(response["content"])
            logger.info(f"Generated {response['type']} for session {sid}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise
    
    def reset_session(self, session_id: Optional[str] = None):
        """Reset a specific session"""
        sid = session_id or self.current_session_id
        if sid in self.store:
            self.store[sid].clear()
        if sid in self.session_states:
            self._init_session_state(sid)
    
    def get_conversation_history(self, session_id: Optional[str] = None) -> List[Dict]:
        """Get conversation history for a session"""
        sid = session_id or self.current_session_id
        history = self.get_session_history(sid)
        
        return [
            {
                "role": "user" if msg.type == "human" else "assistant",
                "content": msg.content
            }
            for msg in history.messages
        ]
    
    def get_diagnostic_summary(self, session_id: Optional[str] = None) -> Dict:
        """Get current diagnostic state summary"""
        sid = session_id or self.current_session_id
        state = self.get_state(sid)
        
        return {
            "questions_asked": state["question_count"],
            "min_required": self.min_questions,
            "max_allowed": self.max_questions,
            "aspects_covered": list(state["aspects_covered"]),
            "top_candidates": [
                {
                    "disease": d["name"],
                    "confidence": d.get("confidence", 0),
                    "evidence_points": state["disease_evidence"].get(d["name"], {}).get("match_count", 0)
                }
                for d in state["potential_diseases"][:3]
            ],
            "is_concluded": state.get("is_concluded", False)
        }
    
    def set_session(self, session_id: str):
        """Switch to a different session"""
        self.current_session_id = session_id
        if session_id not in self.session_states:
            self._init_session_state(session_id)
    
    def should_conclude(self, session_id: str) -> bool:
        """Check if conversation should conclude"""
        state = self.get_state(session_id)
        return state.get("is_concluded", False)
