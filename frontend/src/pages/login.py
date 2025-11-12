import streamlit as st
from ..utils.session_state import set_session_state
from ..utils.conversation_manager import load_conversations

def login_page():
    """Render the login page"""
    st.title("Doctor Session Portal 👨‍⚕️")
    
    with st.form("doctor_session_form"):
        doctor_name = st.text_input("Enter your name", placeholder="Dr. Smith")
        submit_button = st.form_submit_button("Start Session")

    if submit_button:
        if doctor_name:
            set_session_state('doctor_name', doctor_name)
            set_session_state('conversations', load_conversations())
            set_session_state('current_page', 'conversation')
            st.success(f"Welcome, Dr. {doctor_name}!")
            st.balloons()
            st.rerun()
        else:
            st.error("Please enter your name to start the session")