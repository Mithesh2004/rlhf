import streamlit as st
from ..utils.session_state import get_session_state, set_session_state
from ..utils.conversation_manager import get_conversation_stats, add_new_conversation, get_doctor_conversations

def apply_conversation_page_css():
    st.markdown("""
    <style>
    /* Increase max width and improve layout */
    .block-container {
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Style buttons in conversation list */
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
    
    /* Improve spacing */
    .row-widget {
        margin-bottom: 0.5rem;
    }
    
    /* Style text in conversation list */
    .stMarkdown p {
        margin: 0;
        line-height: 40px;  /* Match button height */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Scrollable container */
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
    # Apply custom CSS
    apply_conversation_page_css()
    
    doctor_name = get_session_state('doctor_name')
    st.title(f"Patient Consultation - Dr. {doctor_name}")
    
    # Display conversation statistics at the top
    total_conversations, current_conversation = get_conversation_stats(doctor_name)
    st.subheader(f"Your total conversations: {total_conversations}")
    
    # Create two columns for the layout
    left_col, right_col = st.columns([6, 4])  # 60% left, 40% right
    
    # Left column: Conversation History
    with left_col:
        st.markdown("### Your Previous Conversations")
        conversations = get_doctor_conversations(doctor_name)
        if conversations:
            # Create scrollable container
            with st.container():
                st.markdown('<div class="conversations-container">', unsafe_allow_html=True)
                for conv in reversed(conversations):
                    # Simple one-line display with minimal information
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button(f"#{conv['id']}", key=f"conv_{conv['id']}", 
                                help="Click to open conversation",
                                use_container_width=True):
                            set_session_state('active_conv_id', conv['id'])
                            set_session_state('current_page', 'conversation_detail')
                            st.rerun()
                    with col2:
                        st.write(f"{conv['timestamp']} - {conv['initial_problem'][:50]}{'...' if len(conv['initial_problem']) > 50 else ''}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No previous conversations found")
    
    # Right column: New Conversation Form
    with right_col:
        st.markdown("### Start New Conversation")
        st.markdown(f"Conversation #{current_conversation}")
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # New conversation input
        with st.form("new_conversation"):
            patient_problem = st.text_area(
                "Enter patient's initial problem",
                placeholder="Patient presents with...",
                height=150
            )
            # Add some spacing before the button
            st.markdown("<br>", unsafe_allow_html=True)
            start_conversation = st.form_submit_button("Start New Conversation", type="primary", use_container_width=True)
        
        if start_conversation and patient_problem:
            new_id = add_new_conversation(doctor_name, patient_problem)
            # set active conversation and navigate to detail page
            set_session_state('active_conv_id', new_id)
            set_session_state('current_page', 'conversation_detail')
            st.success("New conversation started!")
            st.rerun()