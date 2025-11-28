import streamlit as st
from ..utils.session_state import get_session_state, set_session_state
from ..utils.api_client import get_api_client


def apply_conversation_page_css():
    st.markdown("""
    <style>
    .block-container {
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .stButton > button {
        height: 40px;
        padding: 0px 16px;
        margin: 0;
        background-color: #f8f9fa;
        border-color: #e0e0e0;
    }
    .stButton > button:hover {
        background-color: #e9ecef;
        border-color: #c0c0c0;
    }
    
    .row-widget {
        margin-bottom: 0.5rem;
    }
    
    .stMarkdown p {
        margin: 0;
        line-height: 40px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .conversations-container {
        max-height: 600px;
        overflow-y: auto;
        padding-right: 10px;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


def conversation_page():
    """Render the conversation page with a two-column layout"""
    apply_conversation_page_css()
    
    doctor_name = get_session_state('doctor_name')
    api_client = get_api_client()
    
    st.title(f"Patient Consultation - Dr. {doctor_name}")
    
    # Get conversations from API
    conversations = api_client.get_doctor_conversations(doctor_name)
    
    # Update session state
    set_session_state('conversations', conversations)
    
    # Display conversation statistics
    total_conversations = len(conversations)
    next_id = (max([c['id'] for c in conversations]) + 1) if conversations else 1
    st.subheader(f"Your total conversations: {total_conversations}")
    
    # Create two columns for the layout
    left_col, right_col = st.columns([6, 4])
    
    # Left column: Conversation History
    with left_col:
        st.markdown("### Your Previous Conversations")
        if conversations:
            with st.container():
                st.markdown('<div class="conversations-container">', unsafe_allow_html=True)
                for conv in reversed(conversations):
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button(f"#{conv['id']}", key=f"conv_{conv['id']}", 
                                help="Click to open conversation",
                                use_container_width=True):
                            set_session_state('active_conv_id', conv['id'])
                            set_session_state('current_page', 'conversation_detail')
                            st.rerun()
                    with col2:
                        problem = conv.get('initial_problem', '')
                        st.write(f"{conv['timestamp']} - {problem[:50]}{'...' if len(problem) > 50 else ''}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No previous conversations found")
    
    # Right column: New Conversation Form
    with right_col:
        st.markdown("### Start New Conversation")
        st.markdown(f"Conversation #{next_id}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("new_conversation"):
            patient_problem = st.text_area(
                "Enter the conversation title",
                placeholder="Patient presents with...",
                height=150
            )
            st.markdown("<br>", unsafe_allow_html=True)
            start_conversation = st.form_submit_button("Start New Conversation", type="primary", use_container_width=True)
        
        if start_conversation and patient_problem:
            # Create conversation via API
            new_conv = api_client.create_conversation(doctor_name, patient_problem)
            
            if new_conv:
                # Update session state
                conversations.append(new_conv)
                set_session_state('conversations', conversations)
                set_session_state('active_conv_id', new_conv['id'])
                set_session_state('current_page', 'conversation_detail')
                st.success("New conversation started!")
                st.rerun()
            else:
                st.error("Failed to create conversation. Please try again.")
