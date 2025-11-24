import streamlit as st
from datetime import datetime
from bson import ObjectId
from .mongodb_config import get_conversations_collection


def save_conversations(conversations):
    """Save conversations to MongoDB - this is now handled per operation"""
    # This function is kept for compatibility but operations are done in real-time
    pass


def load_conversations():
    """Load all conversations from MongoDB"""
    try:
        collection = get_conversations_collection()
        if collection is None:
            return []
        
        conversations = list(collection.find({}))
        
        # Convert ObjectId to string for session state compatibility
        for conv in conversations:
            if '_id' in conv:
                conv['_id'] = str(conv['_id'])
        
        return conversations
    except Exception as e:
        st.error(f"Error loading conversations: {e}")
        return []


def get_doctor_conversations(doctor_name):
    """Get conversations for a specific doctor from MongoDB"""
    try:
        collection = get_conversations_collection()
        if collection is None:
            return []
        
        conversations = list(collection.find({'doctor': doctor_name}))
        
        # Convert ObjectId to string
        for conv in conversations:
            if '_id' in conv:
                conv['_id'] = str(conv['_id'])
        
        return conversations
    except Exception as e:
        st.error(f"Error getting doctor conversations: {e}")
        return []


def get_next_conversation_id(doctor_name):
    """Get the next conversation ID for a specific doctor"""
    doctor_conversations = get_doctor_conversations(doctor_name)
    if not doctor_conversations:
        return 1
    # Get the maximum ID for this doctor and add 1
    max_id = max(conv['id'] for conv in doctor_conversations)
    return max_id + 1


def add_new_conversation(doctor_name, initial_problem):
    """Add a new conversation to MongoDB"""
    try:
        collection = get_conversations_collection()
        if collection is None:
            st.error("Could not connect to database")
            return None
        
        current_conversation = get_next_conversation_id(doctor_name)
        
        new_conversation = {
            'id': current_conversation,
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
                'diagnosis_feedback': ''
            }
        }
        
        # Insert into MongoDB
        result = collection.insert_one(new_conversation)
        new_conversation['_id'] = str(result.inserted_id)
        
        # Update session state
        conversations = st.session_state.get('conversations', [])
        conversations.append(new_conversation)
        st.session_state['conversations'] = conversations
        
        return current_conversation
    except Exception as e:
        st.error(f"Error adding conversation: {e}")
        return None


def get_conversation_stats(doctor_name):
    """Get conversation statistics for a specific doctor"""
    doctor_conversations = get_doctor_conversations(doctor_name)
    total_conversations = len(doctor_conversations)
    current_conversation = get_next_conversation_id(doctor_name)
    return total_conversations, current_conversation


def add_message(conversation_id, sender, message):
    """Add a message to a conversation in MongoDB"""
    try:
        collection = get_conversations_collection()
        if collection is None:
            return False
        
        doctor_name = st.session_state.get('doctor_name')
        
        # Create message dictionary
        message_dict = {
            'sender': sender,
            'content': message,
            'rating': None,
            'priority': None
        }
        
        # Update in MongoDB
        result = collection.update_one(
            {'id': conversation_id, 'doctor': doctor_name},
            {'$push': {'messages': message_dict}}
        )
        
        if result.modified_count > 0:
            # Update session state
            conversations = st.session_state.get('conversations', [])
            for conv in conversations:
                if conv.get('id') == conversation_id and conv.get('doctor') == doctor_name:
                    conv.setdefault('messages', []).append(message_dict)
                    st.session_state['conversations'] = conversations
                    return True
        
        return False
    except Exception as e:
        st.error(f"Error adding message: {e}")
        return False


def update_conversation(conversation_id, doctor_name, updates):
    """Update a conversation in MongoDB"""
    try:
        collection = get_conversations_collection()
        if collection is None:
            return False
        
        result = collection.update_one(
            {'id': conversation_id, 'doctor': doctor_name},
            {'$set': updates}
        )
        
        if result.modified_count > 0:
            # Update session state
            conversations = st.session_state.get('conversations', [])
            for conv in conversations:
                if conv.get('id') == conversation_id and conv.get('doctor') == doctor_name:
                    conv.update(updates)
                    st.session_state['conversations'] = conversations
                    return True
        
        return False
    except Exception as e:
        st.error(f"Error updating conversation: {e}")
        return False


def get_conversation_by_id(conversation_id, doctor_name):
    """Get a specific conversation from MongoDB"""
    try:
        collection = get_conversations_collection()
        if collection is None:
            return None
        
        conversation = collection.find_one({'id': conversation_id, 'doctor': doctor_name})
        
        if conversation and '_id' in conversation:
            conversation['_id'] = str(conversation['_id'])
        
        return conversation
    except Exception as e:
        st.error(f"Error getting conversation: {e}")
        return None
