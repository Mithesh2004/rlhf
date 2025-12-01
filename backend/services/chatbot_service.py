from typing import Optional
import logging
from config import settings
from agents.chatbot import ICMRDiagnosticChatbot

logger = logging.getLogger(__name__)


class ChatbotService:
    """Singleton service for chatbot"""
    
    _instance: Optional[ICMRDiagnosticChatbot] = None
    
    @classmethod
    def get_instance(cls) -> ICMRDiagnosticChatbot:
        """Get or create chatbot instance"""
        if cls._instance is None:
            try:
                cls._instance = ICMRDiagnosticChatbot(
                    qdrant_url=settings.QDRANT_URL,
                    collection_name=settings.QDRANT_COLLECTION,
                    embedding_model=settings.EMBEDDING_MODEL,
                    gemini_model=settings.GEMINI_MODEL,
                    top_k=5,
                    min_questions=int(settings.MIN_QUESTIONS),
                    max_questions=int(settings.MAX_QUESTIONS),
                    confidence_threshold=float(settings.CONFIDENCE_THRESHOLD),
                    mongodb_uri=settings.MONGODB_URI,  # Add MongoDB
                    mongodb_db_name=settings.MONGODB_DB_NAME
                )
                logger.info("✅ Chatbot service initialized with persistent storage")
            except Exception as e:
                logger.error(f"❌ Failed to initialize chatbot: {e}")
                raise
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset chatbot instance"""
        cls._instance = None
        logger.info("Chatbot service reset")
