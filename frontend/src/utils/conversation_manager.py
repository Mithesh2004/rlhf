import json
import os
import streamlit as st
from datetime import datetime


def save_conversations(conversations):
    """Save conversations to a JSON file"""
    os.makedirs('data', exist_ok=True)
    with open('data/conversations.json', 'w') as f:
        json.dump(conversations, f)


def load_conversations():
    """Load conversations from JSON file"""
    try:
        with open('data/conversations.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def get_doctor_conversations(doctor_name):
    """Get conversations for a specific doctor"""
    all_conversations = st.session_state.get('conversations', [])
    return [conv for conv in all_conversations if conv.get('doctor') == doctor_name]


def get_next_conversation_id(doctor_name):
    """Get the next conversation ID for a specific doctor"""
    doctor_conversations = get_doctor_conversations(doctor_name)
    if not doctor_conversations:
        return 1
    # Get the maximum ID for this doctor and add 1
    max_id = max(conv['id'] for conv in doctor_conversations)
    return max_id + 1


def add_new_conversation(doctor_name, initial_problem):
    """Add a new conversation to the list"""
    conversations = st.session_state.get('conversations', [])
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
            'process_notes': ''
        }
    }
    
    conversations.append(new_conversation)
    st.session_state['conversations'] = conversations
    save_conversations(conversations)
    return current_conversation


def get_conversation_stats(doctor_name):
    """Get conversation statistics for a specific doctor"""
    doctor_conversations = get_doctor_conversations(doctor_name)
    total_conversations = len(doctor_conversations)
    current_conversation = get_next_conversation_id(doctor_name)
    return total_conversations, current_conversation


def add_message(conversation_id, sender, message):
    """Add a message to a conversation. Messages are now stored as dictionaries with metadata."""
    conversations = st.session_state.get('conversations', [])
    doctor_name = st.session_state.get('doctor_name')
    
    for conv in conversations:
        # Check both conversation ID and doctor name to ensure we're updating the right conversation
        if conv.get('id') == conversation_id and conv.get('doctor') == doctor_name:
            # Store messages as dictionaries with metadata
            message_dict = {
                'sender': sender,
                'content': message,
                'rating': None,
                'priority': None
            }
            conv.setdefault('messages', []).append(message_dict)
            st.session_state['conversations'] = conversations
            save_conversations(conversations)
            return True
    return False
