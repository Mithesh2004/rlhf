import streamlit as st


def initialize_session_state():
    """Initialize all session state variables"""
    if 'doctor_name' not in st.session_state:
        st.session_state['doctor_name'] = None
    if 'conversations' not in st.session_state:
        st.session_state['conversations'] = []
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'login'
    if 'active_conv_id' not in st.session_state:
        st.session_state['active_conv_id'] = None
    if 'current_conversation' not in st.session_state:
        st.session_state['current_conversation'] = None


def get_session_state(key):
    """Get a session state value"""
    return st.session_state.get(key)


def set_session_state(key, value):
    """Set a session state value"""
    st.session_state[key] = value


def clear_session():
    """Clear the session state"""
    st.session_state['doctor_name'] = None
    st.session_state['current_page'] = 'login'
    st.session_state['conversations'] = []
    st.session_state['active_conv_id'] = None
    st.session_state['current_conversation'] = None
