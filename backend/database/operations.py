from typing import List, Dict, Optional
from datetime import datetime
from bson import ObjectId
from .mongodb import get_conversations_collection


class ConversationOperations:
    """Database operations for conversations"""
    
    @staticmethod
    def create_conversation(doctor_name: str, initial_problem: str) -> Dict:
        """Create a new conversation"""
        collection = get_conversations_collection()
        
        # Get next conversation ID for this doctor
        max_conv = collection.find_one(
            {"doctor": doctor_name},
            sort=[("id", -1)]
        )
        next_id = (max_conv["id"] + 1) if max_conv else 1
        
        new_conversation = {
            'id': next_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'doctor': doctor_name,
            'initial_problem': initial_problem,
            'messages': [],
            'is_ended': False,
            'holistic_feedback': {
                'duration_rating': None,
                'process_notes': '',
                'questions_feedback': ''
            },
            'final_diagnosis': {
                'ai_diagnosis': '',
                'diagnosis_feedback': ''
            }
        }
        
        result = collection.insert_one(new_conversation)
        new_conversation['_id'] = str(result.inserted_id)
        
        return new_conversation
    
    @staticmethod
    def get_doctor_conversations(doctor_name: str) -> List[Dict]:
        """Get all conversations for a doctor"""
        collection = get_conversations_collection()
        conversations = list(collection.find({"doctor": doctor_name}))
        
        for conv in conversations:
            conv['_id'] = str(conv['_id'])
        
        return conversations
    
    @staticmethod
    def get_conversation(doctor_name: str, conversation_id: int) -> Optional[Dict]:
        """Get a specific conversation"""
        collection = get_conversations_collection()
        conversation = collection.find_one({
            "doctor": doctor_name,
            "id": conversation_id
        })
        
        if conversation:
            conversation['_id'] = str(conversation['_id'])
        
        return conversation
    
    @staticmethod
    def add_message(doctor_name: str, conversation_id: int, sender: str, content: str) -> bool:
        """Add a message to conversation"""
        collection = get_conversations_collection()
        
        message = {
            'sender': sender,
            'content': content,
            'rating': None,
            'priority': None
        }
        
        result = collection.update_one(
            {"doctor": doctor_name, "id": conversation_id},
            {"$push": {"messages": message}}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def update_message_rating(doctor_name: str, conversation_id: int, message_index: int, rating: str) -> bool:
        """Update message rating"""
        collection = get_conversations_collection()
        
        result = collection.update_one(
            {"doctor": doctor_name, "id": conversation_id},
            {"$set": {f"messages.{message_index}.rating": rating}}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def update_message_priority(doctor_name: str, conversation_id: int, message_index: int, priority: int) -> bool:
        """Update message priority"""
        collection = get_conversations_collection()
        
        result = collection.update_one(
            {"doctor": doctor_name, "id": conversation_id},
            {"$set": {f"messages.{message_index}.priority": priority}}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def end_conversation(doctor_name: str, conversation_id: int) -> bool:
        """Mark conversation as ended"""
        collection = get_conversations_collection()
        
        result = collection.update_one(
            {"doctor": doctor_name, "id": conversation_id},
            {"$set": {"is_ended": True}}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def update_diagnosis(doctor_name: str, conversation_id: int, ai_diagnosis: str) -> bool:
        """Update AI diagnosis"""
        collection = get_conversations_collection()
        
        result = collection.update_one(
            {"doctor": doctor_name, "id": conversation_id},
            {"$set": {"final_diagnosis.ai_diagnosis": ai_diagnosis}}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def save_diagnosis_feedback(doctor_name: str, conversation_id: int, feedback: str) -> bool:
        """Save diagnosis feedback"""
        collection = get_conversations_collection()
        
        result = collection.update_one(
            {"doctor": doctor_name, "id": conversation_id},
            {"$set": {"final_diagnosis.diagnosis_feedback": feedback}}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def save_conversation_feedback(
        doctor_name: str,
        conversation_id: int,
        questions_feedback: Optional[str] = None,
        duration_rating: Optional[str] = None,
        process_notes: Optional[str] = None
    ) -> bool:
        """Save conversation feedback"""
        collection = get_conversations_collection()
        
        update_fields = {}
        if questions_feedback is not None:
            update_fields["holistic_feedback.questions_feedback"] = questions_feedback
        if duration_rating is not None:
            update_fields["holistic_feedback.duration_rating"] = duration_rating
        if process_notes is not None:
            update_fields["holistic_feedback.process_notes"] = process_notes
        
        if not update_fields:
            return False
        
        result = collection.update_one(
            {"doctor": doctor_name, "id": conversation_id},
            {"$set": update_fields}
        )
        
        return result.modified_count > 0
