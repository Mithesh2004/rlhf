import streamlit as st
from ..utils.session_state import set_session_state
from ..utils.api_client import get_api_client


def login_page():
    """Render the login page"""
    st.title("Doctor Session Portal 👨‍⚕️")
    
    # Check API health
    api_client = get_api_client()
    health = api_client.health_check()
    
    if health.get("status") != "healthy":
        st.error("⚠️ Backend service is not available. Please ensure the backend is running on http://localhost:8000")
        st.info("Start backend with: `cd backend && python main.py`")
        st.stop()
    else:
        st.success("✅ Connected to backend")
    
    with st.form("doctor_session_form"):
        doctor_name = st.text_input("Enter your name", placeholder="Dr. Smith")
        submit_button = st.form_submit_button("Start Session")

    if submit_button:
        if doctor_name:
            # Load doctor's conversations from API
            conversations = api_client.get_doctor_conversations(doctor_name)
            
            set_session_state('doctor_name', doctor_name)
            set_session_state('conversations', conversations)
            set_session_state('current_page', 'conversation')
            st.success(f"Welcome, Dr. {doctor_name}!")
            st.balloons()
            st.rerun()
        else:
            st.error("Please enter your name to start the session")
