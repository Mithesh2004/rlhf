import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from chatbot import ICMRDiagnosticChatbot

def test_chatbot():
    """Test chatbot initialization"""
    try:
        print("Testing chatbot initialization...")
        chatbot = ICMRDiagnosticChatbot(
            qdrant_url="http://localhost:6333",
            collection_name="icmr_data",
            embedding_model="BAAI/bge-small-en-v1.5",
            gemini_model="gemini-2.5-flash",
            top_k=5
        )
        print("✅ Chatbot initialized successfully!")
        
        # Test a simple query
        print("\nTesting chat...")
        response = chatbot.chat("I have a severe headache for 3 days", "test_session")
        print(f"Response: {response[:100]}...")
        print("✅ Chat test successful!")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_chatbot()
