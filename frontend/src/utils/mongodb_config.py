import pymongo
import streamlit as st
from pymongo import MongoClient
from typing import Optional
import os


@st.cache_resource
def init_mongodb_connection() -> MongoClient:
    """Initialize MongoDB Atlas connection with caching"""
    try:
        connection_string = None
        
        # Try 1: Streamlit secrets (for production/deployment)
        try:
            if "mongo" in st.secrets:
                connection_string = st.secrets["mongo"]["connection_string"]
                print("📝 Using connection string from Streamlit secrets")
        except Exception as e:
            print(f"⚠️  No Streamlit secrets found: {e}")
        
        # Try 2: Environment variable
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI')
            if connection_string:
                print("📝 Using connection string from environment variable")
        
        # Try 3: Hardcoded for development (NOT RECOMMENDED for production)
        if connection_string is None:
            # REPLACE THIS WITH YOUR ACTUAL CONNECTION STRING
            connection_string = "mongodb+srv://username:password@cluster.mongodb.net/medical_conversations_db?retryWrites=true&w=majority"
            print("📝 Using hardcoded connection string (development only)")
        
        if connection_string is None:
            raise Exception("No MongoDB connection string found")
        
        # Create client
        client = MongoClient(
            connection_string,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsAllowInvalidCertificates=False
        )
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        return client
    
    except pymongo.errors.ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
        return None
    except pymongo.errors.ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def get_database():
    """Get the database instance"""
    client = init_mongodb_connection()
    if client is not None:  # CRITICAL FIX: Use 'is not None'
        return client['medical_conversations_db']
    return None


def get_conversations_collection():
    """Get the conversations collection"""
    db = get_database()
    if db is not None:  # CRITICAL FIX: Use 'is not None' instead of 'if db:'
        return db['conversations']
    return None


def test_connection():
    """Test MongoDB Atlas connection"""
    try:
        client = init_mongodb_connection()
        if client is not None:  # CRITICAL FIX
            db = get_database()
            if db is not None:  # CRITICAL FIX
                print(f"✅ Connected to database: {db.name}")
                
                # List collections
                collections = db.list_collection_names()
                print(f"✅ Collections: {collections}")
                
                return True
        return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False
