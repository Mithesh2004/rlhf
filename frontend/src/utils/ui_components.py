import streamlit as st


def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        margin-top: 20px;
    }
    .conversation-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


def setup_page_config():
    """Configure the page settings"""
    st.set_page_config(
        page_title="Doctor Session Portal",
        page_icon="👨‍⚕️",
        layout="wide"
    )
