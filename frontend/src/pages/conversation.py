import streamlit as st
from ..utils.session_state import get_session_state, set_session_state, clear_session
from ..utils.api_client import get_api_client


def conversation_page():
    """Render the conversation management page"""
    doctor_name = get_session_state('doctor_name')
    api_client = get_api_client()
    
    # Header with logout button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"Welcome, Dr. {doctor_name}! 👨‍⚕️")
    with col2:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            clear_session()
            st.rerun()
    
    st.markdown("---")
    
    # Get conversations from API
    conversations = api_client.get_doctor_conversations(doctor_name)
    set_session_state('conversations', conversations)
    
    # Statistics
    total_conversations = len(conversations)
    active_conversations = len([c for c in conversations if not c.get('is_ended', False)])
    completed_conversations = len([c for c in conversations if c.get('is_ended', False)])
    
    # Display stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Conversations", total_conversations)
    with col2:
        st.metric("Active", active_conversations)
    with col3:
        st.metric("Completed", completed_conversations)
    
    st.markdown("---")
    
    # Start new conversation section with input
    st.markdown("### 🆕 Start New Conversation")
    
    with st.form("new_conversation_form", clear_on_submit=True):
        initial_problem = st.text_area(
            "Patient's chief complaint:",
            placeholder="e.g., Persistent headache",
            height=80
        )
        
        submit_button = st.form_submit_button("➕ Create Conversation", 
                                               type="primary", 
                                               use_container_width=True)
        
        if submit_button:
            if initial_problem and initial_problem.strip():
                # Create new conversation via API
                new_conv = api_client.create_conversation(doctor_name, initial_problem.strip())
                
                if new_conv:
                    st.success(f"✅ Conversation #{new_conv['id']} created!")
                    set_session_state('active_conv_id', new_conv['id'])
                    set_session_state('current_page', 'conversation_detail')
                    st.rerun()
                else:
                    st.error("❌ Failed to create conversation.")
            else:
                st.warning("⚠️ Please enter a description.")

    
    st.markdown("---")
    st.markdown("### 📋 Your Previous Conversations")
    
    # Custom CSS for scrollable container
    st.markdown("""
    <style>
    .scrollable-container {
        max-height: 500px;
        overflow-y: auto;
        padding-right: 10px;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        background-color: #f9f9f9;
    }
    
    /* Webkit browsers (Chrome, Safari) */
    .scrollable-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .scrollable-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .scrollable-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    
    .scrollable-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    .conversation-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #007AFF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .conversation-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .conversation-card-ended {
        border-left-color: #28a745;
    }
    
    .conversation-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .conversation-title {
        font-size: 18px;
        font-weight: bold;
        color: #333;
    }
    
    .conversation-status {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .status-active {
        background-color: #fff3cd;
        color: #856404;
    }
    
    .status-completed {
        background-color: #d4edda;
        color: #155724;
    }
    
    .conversation-meta {
        color: #666;
        font-size: 14px;
        margin-top: 5px;
    }
    
    .conversation-problem {
        color: #555;
        font-size: 14px;
        margin-top: 8px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if conversations:
        # Start scrollable container
        st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
        
        # Sort conversations: active first, then by ID descending
        sorted_conversations = sorted(
            conversations,
            key=lambda x: (x.get('is_ended', False), -x.get('id', 0))
        )
        
        for conv in sorted_conversations:
            is_ended = conv.get('is_ended', False)
            conv_id = conv.get('id', 0)
            timestamp = conv.get('timestamp', 'N/A')
            initial_problem = conv.get('initial_problem', 'No description')
            messages = conv.get('messages', [])
            message_count = len(messages)
            
            # Determine status
            status_class = "status-completed" if is_ended else "status-active"
            status_text = "✅ Completed" if is_ended else "🔄 Active"
            card_class = "conversation-card-ended" if is_ended else ""
            
            # Render conversation card
            st.markdown(f"""
            <div class="conversation-card {card_class}">
                <div class="conversation-header">
                    <div class="conversation-title">Conversation #{conv_id}</div>
                    <div class="conversation-status {status_class}">{status_text}</div>
                </div>
                <div class="conversation-meta">
                    📅 {timestamp} | 💬 {message_count} messages
                </div>
                <div class="conversation-problem">
                    "{initial_problem[:100]}{'...' if len(initial_problem) > 100 else ''}"
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Button to open conversation
            if st.button(f"Open Conversation #{conv_id}", 
                        key=f"open_conv_{conv_id}",
                        use_container_width=True):
                set_session_state('active_conv_id', conv_id)
                set_session_state('current_page', 'conversation_detail')
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # End scrollable container
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📭 No conversations yet. Create your first conversation above!")
    
    st.markdown("---")
    
    # Footer
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption("💡 Tip: Active conversations appear first. Completed ones are marked with ✅")
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
