from pymongo import MongoClient
from typing import Optional
import sys
sys.path.append('..')
from config import settings


class MongoDB:
    _client: Optional[MongoClient] = None
    _db = None
    
    @classmethod
    def connect(cls):
        """Initialize MongoDB connection"""
        if cls._client is None:
            try:
                cls._client = MongoClient(
                    settings.MONGODB_URI,
                    serverSelectionTimeoutMS=5000,
                    tls=True,
                    tlsAllowInvalidCertificates=False
                )
                cls._client.admin.command('ping')
                cls._db = cls._client[settings.MONGODB_DB_NAME]
                print(f"✅ Connected to MongoDB: {settings.MONGODB_DB_NAME}")
            except Exception as e:
                print(f"❌ MongoDB connection failed: {e}")
                raise
        return cls._db
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        if cls._db is None:
            return cls.connect()
        return cls._db
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get a specific collection"""
        db = cls.get_database()
        if db is not None:
            return db[collection_name]
        return None
    
    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None
            print("✅ MongoDB connection closed")


# Convenience function
def get_conversations_collection():
    """Get conversations collection"""
    return MongoDB.get_collection("conversations")
