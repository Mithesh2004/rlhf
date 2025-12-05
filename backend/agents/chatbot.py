import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Set, Literal
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from pymongo import MongoClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class MongoDBChatMessageHistory(BaseChatMessageHistory):
    """Chat message history stored in MongoDB"""
    
    def __init__(self, session_id: str, mongo_client: MongoClient, db_name: str):
        self.session_id = session_id
        self.collection = mongo_client[db_name]["chat_histories"]
        self._messages = None
    
    @property
    def messages(self) -> List[BaseMessage]:
        """Retrieve messages from MongoDB"""
        if self._messages is None:
            doc = self.collection.find_one({"session_id": self.session_id})
            if doc and "messages" in doc:
                self._messages = []
                for msg_data in doc["messages"]:
                    if msg_data["type"] == "human":
                        self._messages.append(HumanMessage(content=msg_data["content"]))
                    else:
                        self._messages.append(AIMessage(content=msg_data["content"]))
            else:
                self._messages = []
        return self._messages
    
    def add_message(self, message: BaseMessage) -> None:
        """Add a message to MongoDB"""
        msg_data = {
            "type": "human" if isinstance(message, HumanMessage) else "ai",
            "content": message.content,
            "timestamp": datetime.utcnow()
        }
        
        self.collection.update_one(
            {"session_id": self.session_id},
            {
                "$push": {"messages": msg_data},
                "$set": {"updated_at": datetime.utcnow()}
            },
            upsert=True
        )
        
        # Update cache
        if self._messages is not None:
            self._messages.append(message)
    
    def clear(self) -> None:
        """Clear messages from MongoDB"""
        self.collection.delete_one({"session_id": self.session_id})
        self._messages = []


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
        top_k: int = 5,
        min_questions: int = 5,
        max_questions: int = 15,
        confidence_threshold: float = 0.85,
        mongodb_uri: str = None,
        mongodb_db_name: str = "medical_conversations_db"
    ):
        """Initialize the diagnostic chatbot with Qdrant and Gemini"""
        logger.info("Initializing ICMR Diagnostic Chatbot...")
        
        # Store configuration
        self.min_questions = min_questions
        self.max_questions = max_questions
        self.confidence_threshold = confidence_threshold
        
        # Initialize MongoDB for persistent storage
        self.mongo_client = None
        self.mongodb_db_name = mongodb_db_name
        self.use_mongodb = False
        
        if mongodb_uri:
            try:
                self.mongo_client = MongoClient(mongodb_uri)
                # Test connection
                self.mongo_client.admin.command('ping')
                self.session_states_collection = self.mongo_client[mongodb_db_name]["session_states"]
                self.use_mongodb = True
                logger.info("✅ Connected to MongoDB for persistent storage")
            except Exception as e:
                logger.warning(f"⚠️  MongoDB connection failed, using in-memory storage: {e}")
                self.use_mongodb = False
        
        # Fallback to in-memory if MongoDB not available
        if not self.use_mongodb:
            self.store = {}
            self.session_states = {}
            logger.info("Using in-memory storage (not persistent)")
        
        # Initialize Qdrant client
        try:
            self.client = QdrantClient(url=qdrant_url)
            self.collection_name = collection_name
            collections = self.client.get_collections()
            logger.info(f"✅ Connected to Qdrant at {qdrant_url}")
            
            collection_names = [col.name for col in collections.collections]
            if collection_name not in collection_names:
                logger.warning(f"⚠️  Collection '{collection_name}' not found")
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
            logger.error("❌ GOOGLE_API_KEY not found")
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
        self.current_session_id = "default_session"
        
        # Build chains
        self._build_chains()
        
        logger.info("✅ Chatbot initialization complete")
    
    def _init_session_state(self, session_id: str):
        """Initialize state for a new session"""
        initial_state = {
            "session_id": session_id,
            "initial_symptoms": [],
            "asked_questions": [],
            "asked_categories": [],
            "potential_diseases": [],
            "question_count": 0,
            "current_context": [],
            "aspects_covered": [],
            "disease_evidence": {},
            "is_concluded": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        if self.use_mongodb:
            self.session_states_collection.update_one(
                {"session_id": session_id},
                {"$set": initial_state},
                upsert=True
            )
        else:
            self.session_states[session_id] = initial_state
        
        logger.debug(f"Initialized session state for: {session_id}")
    
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create chat history for a session"""
        if self.use_mongodb:
            return MongoDBChatMessageHistory(session_id, self.mongo_client, self.mongodb_db_name)
        else:
            # Fallback to in-memory
            from langchain_core.chat_history import InMemoryChatMessageHistory
            if session_id not in self.store:
                self.store[session_id] = InMemoryChatMessageHistory()
            return self.store[session_id]
    
    def get_state(self, session_id: Optional[str] = None) -> Dict:
        """Get current session state"""
        sid = session_id or self.current_session_id
        
        if self.use_mongodb:
            doc = self.session_states_collection.find_one({"session_id": sid})
            if doc:
                # Convert sets back from lists
                if "aspects_covered" in doc and isinstance(doc["aspects_covered"], list):
                    doc["aspects_covered"] = set(doc["aspects_covered"])
                if "asked_categories" in doc and isinstance(doc["asked_categories"], list):
                    doc["asked_categories"] = set(doc["asked_categories"])
                return doc
            else:
                self._init_session_state(sid)
                return self.get_state(sid)
        else:
            if sid not in self.session_states:
                self._init_session_state(sid)
            return self.session_states.get(sid, {})
    
    def update_state(self, session_id: str, updates: Dict):
        """Update session state"""
        if self.use_mongodb:
            # Convert sets to lists for MongoDB
            mongo_updates = {}
            for key, value in updates.items():
                if isinstance(value, set):
                    mongo_updates[key] = list(value)
                else:
                    mongo_updates[key] = value
            
            mongo_updates["updated_at"] = datetime.utcnow()
            
            self.session_states_collection.update_one(
                {"session_id": session_id},
                {"$set": mongo_updates},
                upsert=True
            )
        else:
            if session_id in self.session_states:
                self.session_states[session_id].update(updates)
    
    # Keep all other methods the same, but update get_state() calls to also call update_state()
    # For example, in analyze_symptoms, refine_diagnosis, etc.
    
    def _build_chains(self):
        """Build LangChain chains with message history"""
        
        # Question generation chain with structured output
        self.question_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert medical diagnostician using ICMR clinical guidelines. Your role is to ask ONE targeted question OR provide a final diagnosis.

**PATIENT DEMOGRAPHICS:**
{patient_demographics}

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
  "content": "## Possible Conditions\\n[Full diagnosis with all sections]\\n## Recommended Actions\\n...",
  "reasoning": "Sufficient information gathered"
}}

**CRITICAL**: Your response must be ONLY the JSON object, nothing else."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "Based on the patient's demographics, input and ICMR data, decide: ask a question OR provide diagnosis. Respond ONLY with JSON.")
        ])
#   "content": "## Possible Conditions\\n[Full diagnosis with all sections]\\n## Recommended Actions\\n...\\n## Further Evaluation\\n...\\n## Department Referral\\n...\\n## Urgency Level\\n...",
    
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
    
    def determine_next_category(self, state: Dict) -> str:
        """Determine which aspect to ask about next"""
        priority_categories = [
            "temporal", "severity", "location", "character", 
            "associated", "modifying", "history"
        ]
        
        covered = state.get("aspects_covered", [])
        if isinstance(covered, list):
            covered = set(covered)
        
        for category in priority_categories:
            if category not in covered:
                return category
        
        return "differential"
    
    def calculate_confidence(self, disease_name: str, state: Dict) -> float:
        """Calculate confidence for a disease"""
        evidence = state.get("disease_evidence", {}).get(disease_name, {})
        base_score = evidence.get("avg_score", 0)
        match_count = evidence.get("match_count", 0)
        
        question_count = state.get("question_count", 0)
        aspects_covered = state.get("aspects_covered", [])
        if isinstance(aspects_covered, list):
            aspects_covered_count = len(aspects_covered)
        else:
            aspects_covered_count = len(list(aspects_covered))
        
        # Adjust confidence
        question_penalty = min(question_count / self.min_questions, 1.0)
        aspect_bonus = min(aspects_covered_count / 5, 1.0)
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
        
        disease_evidence = state.get("disease_evidence", {})
        for disease, data in disease_scores.items():
            avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
            disease_evidence[disease] = {
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
        
        potential_diseases = [{"name": d[0], **d[1]} for d in sorted_diseases]
        
        # Update state
        self.update_state(session_id, {
            "potential_diseases": potential_diseases,
            "current_context": results,
            "disease_evidence": disease_evidence
        })
        
        return {"candidates": potential_diseases, "context": results}
    
    def refine_diagnosis(self, new_info: str, session_id: str) -> None:
        """Refine potential diseases based on new information"""
        state = self.get_state(session_id)
        
        initial_symptoms = state.get("initial_symptoms", [])
        all_info = " ".join(initial_symptoms) + " " + new_info
        
        question_count = state.get("question_count", 0)
        potential_diseases = state.get("potential_diseases", [])
        
        # Progressive filtering
        filters = None
        if question_count > 5 and potential_diseases:
            disease_names = [d["name"] for d in potential_diseases[:3]]
            filters = {
                "should": [
                    {"key": "disease", "match": {"value": disease}}
                    for disease in disease_names
                ]
            }
        
        results = self.search_qdrant(all_info, filters)
        
        disease_evidence = state.get("disease_evidence", {})
        
        # Update disease evidence
        for result in results:
            disease = result["disease"]
            if disease:
                if disease in disease_evidence:
                    existing = disease_evidence[disease]
                    existing["avg_score"] = (existing["avg_score"] + result["score"]) / 2
                    existing["match_count"] += 1
                else:
                    disease_evidence[disease] = {
                        "avg_score": result["score"],
                        "match_count": 1,
                        "sections": [result["header"]]
                    }
        
        # Recalculate top diseases
        disease_confidences = {}
        for disease in disease_evidence:
            confidence = self.calculate_confidence(disease, state)
            disease_confidences[disease] = {
                "name": disease,
                "confidence": confidence * 100,
                "match_count": disease_evidence[disease]["match_count"]
            }
        
        sorted_diseases = sorted(
            disease_confidences.items(),
            key=lambda x: x[1]["confidence"],
            reverse=True
        )[:3]
        
        updated_diseases = [d[1] for d in sorted_diseases]
        
        # Update state
        self.update_state(session_id, {
            "potential_diseases": updated_diseases,
            "current_context": results,
            "disease_evidence": disease_evidence
        })
    
    def generate_response(self, session_id: str) -> Dict:
        """Generate next response (question or diagnosis)"""
        state = self.get_state(session_id)
        
        # Get patient demographics
        patient_age = state.get("patient_age", "Unknown")
        patient_gender = state.get("patient_gender", "Unknown")
        patient_demographics = f"Patient: {patient_age} year old {patient_gender}"
        
        # Prepare context
        current_context = state.get("current_context", [])
        context_text = "\n\n".join([
            f"Disease: {doc['disease']}\n"
            f"Section: {doc['header']}\n"
            f"Content: {doc['text'][:400]}\n"
            f"Relevance: {doc['score']:.2f}"
            for doc in current_context[:5]
        ])
        
        potential_diseases = state.get("potential_diseases", [])
        candidates = ", ".join([
            f"{d['name']} ({d.get('confidence', 0):.1f}%)"
            for d in potential_diseases[:3]
        ])
        
        asked_questions = state.get("asked_questions", [])
        asked_questions_text = "\n".join(asked_questions[-5:])
        
        aspects_covered = state.get("aspects_covered", [])
        if isinstance(aspects_covered, list):
            aspects_covered = set(aspects_covered)
        
        all_aspects = {"temporal", "severity", "location", "character", "associated", "modifying", "history"}
        uncovered = all_aspects - aspects_covered
        uncovered_text = ", ".join(uncovered) if uncovered else "All aspects covered"
        
        current_category = self.determine_next_category(state)
        question_count = state.get("question_count", 0)
        
        # Generate response
        try:
            response = self.question_with_history.invoke(
                {
                    "input": "generate next response",
                    "patient_demographics": patient_demographics,
                    "context": context_text if context_text else "No specific ICMR data retrieved yet.",
                    "candidates": candidates if candidates else "Analyzing initial symptoms...",
                    "asked_questions": asked_questions_text if asked_questions_text else "None",
                    "current_category": current_category,
                    "uncovered_aspects": uncovered_text,
                    "question_count": question_count,
                    "max_questions": self.max_questions,
                    "min_questions": self.min_questions,
                    "aspects_covered": len(aspects_covered),
                    "confidence_threshold": int(self.confidence_threshold * 100)
                },
                config={"configurable": {"session_id": session_id}}
            )
            
            if isinstance(response, dict) and "type" in response and "content" in response:
                return response
            else:
                logger.warning("Response not in expected format")
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
    
    def chat(self, user_input: str, session_id: Optional[str] = None, patient_age: Optional[int] = None, patient_gender: Optional[str] = None) -> Dict:
        """Main chat interface - returns structured response"""
        try:
            sid = session_id or self.current_session_id
            
            state = self.get_state(sid)
            
            # Check if this is a new session
            if not state or state.get("question_count", 0) == 0:
                self._init_session_state(sid)
                state = self.get_state(sid)
                
                # Store patient demographics in session state
                if patient_age and patient_gender:
                    self.update_state(sid, {
                        "patient_age": patient_age,
                        "patient_gender": patient_gender
                    })
    
            
            history = self.get_session_history(sid)
            history.add_user_message(user_input)
            
            question_count = state.get("question_count", 0)
            
            # First message: analyze symptoms
            if question_count == 0:
                initial_symptoms = state.get("initial_symptoms", [])
                initial_symptoms.append(user_input)
                self.update_state(sid, {"initial_symptoms": initial_symptoms})
                self.analyze_symptoms(user_input, sid)
            else:
                # Subsequent messages: refine diagnosis
                self.refine_diagnosis(user_input, sid)
            
            # Generate response
            response = self.generate_response(sid)
            
            # Update state based on response type
            state = self.get_state(sid)  # Refresh state
            if response["type"] == "question":
                question_count = state.get("question_count", 0) + 1
                asked_questions = state.get("asked_questions", [])
                asked_questions.append(response["content"])
                
                category = self.determine_next_category(state)
                aspects_covered = state.get("aspects_covered", [])
                if isinstance(aspects_covered, list):
                    aspects_covered = set(aspects_covered)
                aspects_covered.add(category)
                
                self.update_state(sid, {
                    "question_count": question_count,
                    "asked_questions": asked_questions,
                    "aspects_covered": list(aspects_covered)
                })
            else:
                self.update_state(sid, {"is_concluded": True})
            
            history.add_ai_message(response["content"])
            logger.info(f"Generated {response['type']} for session {sid}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise
    
    def reset_session(self, session_id: Optional[str] = None):
        """Reset a specific session"""
        sid = session_id or self.current_session_id
        
        history = self.get_session_history(sid)
        history.clear()
        
        if self.use_mongodb:
            self.session_states_collection.delete_one({"session_id": sid})
        else:
            if sid in self.session_states:
                del self.session_states[sid]
        
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
        
        potential_diseases = state.get("potential_diseases", [])
        disease_evidence = state.get("disease_evidence", {})
        aspects_covered = state.get("aspects_covered", [])
        
        return {
            "questions_asked": state.get("question_count", 0),
            "min_required": self.min_questions,
            "max_allowed": self.max_questions,
            "aspects_covered": list(aspects_covered) if isinstance(aspects_covered, set) else aspects_covered,
            "top_candidates": [
                {
                    "disease": d["name"],
                    "confidence": d.get("confidence", 0),
                    "evidence_points": disease_evidence.get(d["name"], {}).get("match_count", 0)
                }
                for d in potential_diseases[:3]
            ],
            "is_concluded": state.get("is_concluded", False)
        }
    
    def set_session(self, session_id: str):
        """Switch to a different session"""
        self.current_session_id = session_id
        state = self.get_state(session_id)
        if not state or not state.get("session_id"):
            self._init_session_state(session_id)
    
    def should_conclude(self, session_id: str) -> bool:
        """Check if conversation should conclude"""
        state = self.get_state(session_id)
        return state.get("is_concluded", False)
