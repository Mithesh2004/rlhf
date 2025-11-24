import requests
from typing import Dict, Optional, List
import streamlit as st


class DiagnosticAPIClient:
    """Client for communicating with the FastAPI backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict:
        """Check if API is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    # Conversation Management
    def create_conversation(self, doctor_name: str, initial_problem: str) -> Optional[Dict]:
        """Create new conversation via API"""
        try:
            response = self.session.post(
                f"{self.base_url}/conversations/create",
                json={"doctor_name": doctor_name, "initial_problem": initial_problem},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Failed to create conversation: {e}")
            return None
    
    def get_doctor_conversations(self, doctor_name: str) -> List[Dict]:
        """Get all conversations for a doctor"""
        try:
            response = self.session.get(
                f"{self.base_url}/conversations/{doctor_name}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Failed to get conversations: {e}")
            return []
    
    def get_conversation(self, doctor_name: str, conversation_id: int) -> Optional[Dict]:
        """Get specific conversation"""
        try:
            response = self.session.get(
                f"{self.base_url}/conversations/{doctor_name}/{conversation_id}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Failed to get conversation: {e}")
            return None
    
    def add_message(self, doctor_name: str, conversation_id: int, sender: str, content: str) -> bool:
        """Add a message to conversation"""
        try:
            response = self.session.post(
                f"{self.base_url}/conversations/message/add",
                json={
                    "doctor_name": doctor_name,
                    "conversation_id": conversation_id,
                    "sender": sender,
                    "content": content
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except Exception as e:
            st.error(f"Failed to add message: {e}")
            return False
    
    def end_conversation(self, doctor_name: str, conversation_id: int) -> bool:
        """Mark conversation as ended"""
        try:
            response = self.session.post(
                f"{self.base_url}/conversations/end",
                params={"doctor_name": doctor_name, "conversation_id": conversation_id},
                timeout=5
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except Exception as e:
            st.error(f"Failed to end conversation: {e}")
            return False
    
    # Chat Operations
    def send_message(
        self,
        message: str,
        session_id: str,
        doctor_name: str,
        conversation_id: int
    ) -> Optional[Dict]:
        """Send a message to the chatbot"""
        try:
            payload = {
                "message": message,
                "session_id": session_id,
                "doctor_name": doctor_name,
                "conversation_id": conversation_id
            }
            
            response = self.session.post(
                f"{self.base_url}/chat/",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
            return None
    
    def reset_session(self, session_id: str) -> bool:
        """Reset a conversation session"""
        try:
            response = self.session.post(
                f"{self.base_url}/chat/reset",
                params={"session_id": session_id},
                timeout=5
            )
            response.raise_for_status()
            return True
        except Exception as e:
            st.error(f"Failed to reset session: {e}")
            return False
    
    def get_status(self, session_id: str) -> Optional[Dict]:
        """Get diagnostic status"""
        try:
            response = self.session.get(
                f"{self.base_url}/chat/status/{session_id}",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Failed to get status: {e}")
            return None
    
    def get_final_diagnosis(self, doctor_name: str, conversation_id: int) -> Optional[Dict]:
        """Get the final diagnosis for a conversation"""
        try:
            response = self.session.get(
                f"{self.base_url}/chat/diagnosis/{doctor_name}/{conversation_id}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # Don't show error for this - it's expected when diagnosis doesn't exist yet
            return {
                "diagnosis": "",
                "is_available": False,
                "is_ended": False
            }
    
    # Feedback Operations
    def update_message_rating(
        self,
        doctor_name: str,
        conversation_id: int,
        message_index: int,
        rating: str
    ) -> bool:
        """Update message rating"""
        try:
            response = self.session.post(
                f"{self.base_url}/feedback/message/rating",
                json={
                    "doctor_name": doctor_name,
                    "conversation_id": conversation_id,
                    "message_index": message_index,
                    "rating": rating
                },
                timeout=5
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except Exception as e:
            st.error(f"Failed to update rating: {e}")
            return False
    
    def update_message_priority(
        self,
        doctor_name: str,
        conversation_id: int,
        message_index: int,
        priority: int
    ) -> bool:
        """Update message priority"""
        try:
            response = self.session.post(
                f"{self.base_url}/feedback/message/priority",
                json={
                    "doctor_name": doctor_name,
                    "conversation_id": conversation_id,
                    "message_index": message_index,
                    "priority": priority
                },
                timeout=5
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except Exception as e:
            st.error(f"Failed to update priority: {e}")
            return False
    
    def save_diagnosis_feedback(
        self,
        doctor_name: str,
        conversation_id: int,
        feedback: str
    ) -> bool:
        """Save diagnosis feedback"""
        try:
            response = self.session.post(
                f"{self.base_url}/feedback/diagnosis",
                json={
                    "doctor_name": doctor_name,
                    "conversation_id": conversation_id,
                    "diagnosis_feedback": feedback
                },
                timeout=5
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except Exception as e:
            st.error(f"Failed to save feedback: {e}")
            return False
    
    def save_conversation_feedback(
        self,
        doctor_name: str,
        conversation_id: int,
        questions_feedback: Optional[str] = None,
        duration_rating: Optional[str] = None,
        process_notes: Optional[str] = None
    ) -> bool:
        """Save conversation feedback"""
        try:
            response = self.session.post(
                f"{self.base_url}/feedback/conversation",
                json={
                    "doctor_name": doctor_name,
                    "conversation_id": conversation_id,
                    "questions_feedback": questions_feedback,
                    "duration_rating": duration_rating,
                    "process_notes": process_notes
                },
                timeout=5
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except Exception as e:
            st.error(f"Failed to save feedback: {e}")
            return False


# Global API client instance
@st.cache_resource
def get_api_client():
    """Get cached API client instance"""
    return DiagnosticAPIClient(base_url="http://localhost:8000")
