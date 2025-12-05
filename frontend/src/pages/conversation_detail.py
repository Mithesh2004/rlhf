import streamlit as st
from ..utils.session_state import get_session_state, set_session_state, clear_session
from ..utils.api_client import get_api_client


def apply_chat_css():
    """Apply custom CSS for chat interface"""
    st.markdown("""
    <style>
    
    .message {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 85%;
        word-wrap: break-word;
    }
    .doctor-message {
        float: right;
        background-color: #007AFF;
        color: white;
        border-bottom-right-radius: 5px;
    }
    .ai-message {
        float: left;
        background-color: #E9ECEF;
        color: black;
        border-bottom-left-radius: 5px;
    }
    .message-container {
        margin: 10px 0 2px 0;
        clear: both;
    }
    .system-message {
        width: 100%;
        text-align: center;
        margin: 10px 0;
        padding: 10px;
        background-color: #e8f4f8;
        border-radius: 5px;
        color: #1a73e8;
        font-weight: 500;
    }
    .conversation-ended {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        text-align: center;
    }
    .diagnosis-ready-banner {
        background-color: #d4edda;
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        text-align: center;
        font-weight: 500;
    }
    
    /* Typing indicator animation */
    .typing-indicator {
        display: flex;
        align-items: center;
        padding: 5px 0;
    }
    
    .typing-indicator span {
        height: 8px;
        width: 8px;
        background-color: #90949c;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        animation: typing 1.4s infinite;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.5;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    
    .section-header {
        background-color: #f0f2f6;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #007AFF;
    }
    
    .section-header-diagnosis {
        border-left-color: #28a745;
    }
    </style>
    """, unsafe_allow_html=True)


def count_ai_messages(messages):
    """Count the number of AI messages (excluding system messages)"""
    count = 0
    for msg in messages:
        if isinstance(msg, dict):
            if msg.get('sender') == 'AI':
                count += 1
        else:
            if msg.startswith('AI: '):
                count += 1
    return count


def render_message(sender, content, message_index=None, conv=None):
    """Render a chat message with the appropriate styling"""
    if sender == "System":
        st.markdown(f'<div class="system-message">🤖 {content}</div>', unsafe_allow_html=True)
    else:
        css_class = "doctor-message" if sender == "Doctor" else "ai-message"
        content_escaped = content.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        st.markdown(f"""
        <div class="message-container">
            <div class="message {css_class}">
                {content_escaped}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add rating and priority buttons only for AI messages from database
        if sender == "AI" and message_index is not None and conv is not None:
            doctor_name = get_session_state('doctor_name')
            api_client = get_api_client()
            
            message_data = conv['messages'][message_index]
            if isinstance(message_data, dict):
                current_rating = message_data.get('rating')
                current_priority = message_data.get('priority')
            else:
                current_rating = None
                current_priority = None
            
            total_ai_messages = count_ai_messages(conv.get('messages', []))
            
            priority_owners = {}
            for idx, msg in enumerate(conv.get('messages', [])):
                if isinstance(msg, dict) and msg.get('sender') == 'AI':
                    if msg.get('priority') is not None:
                        priority_owners[msg.get('priority')] = idx
            
            col1, col2, col3 = st.columns([1, 1, 4])
            
            with col1:
                if st.button("👍🏼", key=f"relevant_{message_index}",
                           help="Relevant", use_container_width=True,
                           type="primary" if current_rating == "relevant" else "secondary"):
                    if api_client.update_message_rating(doctor_name, conv['id'], message_index, "relevant"):
                        st.rerun()
            
            with col2:
                if st.button("👎🏼", key=f"irrelevant_{message_index}",
                           help="Irrelevant", use_container_width=True,
                           type="primary" if current_rating == "irrelevant" else "secondary"):
                    if api_client.update_message_rating(doctor_name, conv['id'], message_index, "irrelevant"):
                        st.rerun()
                    
            with col3:
                if current_priority is not None:
                    button_label = f"⭐ P{current_priority}"
                else:
                    button_label = "⚠️ Priority"
                
                with st.popover(button_label, use_container_width=False):
                    st.markdown("**Set Priority Rank**")
                    st.caption(f"1 = Highest, {total_ai_messages} = Lowest")
                    
                    for row_start in range(1, total_ai_messages + 1, 5):
                        cols = st.columns(min(5, total_ai_messages - row_start + 1))
                        for i, col in enumerate(cols):
                            priority_num = row_start + i
                            if priority_num <= total_ai_messages:
                                with col:
                                    is_assigned_elsewhere = priority_num in priority_owners and priority_owners[priority_num] != message_index
                                    is_current = current_priority == priority_num
                                    
                                    button_type = "primary" if is_current else "secondary"
                                    
                                    button_label_text = str(priority_num)
                                    if is_assigned_elsewhere:
                                        button_label_text += f"*"
                                        help_text = f"Assigned elsewhere. Click to reassign."
                                    elif is_current:
                                        help_text = f"Current priority"
                                    else:
                                        help_text = f"Set priority {priority_num}"
                                    
                                    if st.button(
                                        button_label_text,
                                        key=f"priority_{priority_num}_{message_index}",
                                        use_container_width=True,
                                        type=button_type,
                                        help=help_text
                                    ):
                                        if is_assigned_elsewhere:
                                            if api_client.reassign_message_priority(doctor_name, conv['id'], message_index, priority_num):
                                                st.rerun()
                                        else:
                                            if api_client.update_message_priority(doctor_name, conv['id'], message_index, priority_num):
                                                st.rerun()
                    
                    if current_priority is not None:
                        st.divider()
                        if st.button("❌ Clear", key=f"clear_{message_index}", use_container_width=True):
                            if api_client.update_message_priority(doctor_name, conv['id'], message_index, 0):
                                st.rerun()


def render_conversation_feedback(conv):
    """Render conversation feedback panel (right side, parallel to chat)"""
    feedback = conv.get('holistic_feedback', {})
    api_client = get_api_client()
    doctor_name = get_session_state('doctor_name')
    
    # Check what feedback exists
    has_questions_feedback = bool(feedback.get('questions_feedback', '').strip())
    has_duration_rating = bool(feedback.get('duration_rating'))
    has_process_notes = bool(feedback.get('process_notes', '').strip())
    
    # Header with progress
    completed = sum([has_questions_feedback, has_duration_rating, has_process_notes])
    total = 3
    
    st.markdown('<div class="section-header">💬 Conversation Feedback</div>', unsafe_allow_html=True)
    
    if completed == total:
        st.success(f"✅ Complete ({completed}/{total})")
    else:
        st.info(f"📊 Progress: {completed}/{total}")
    
    # Section 1: Missed Questions - collapsed by default
    with st.expander(f"📋 Missed Questions {'✅' if has_questions_feedback else '⏳'}", expanded=False):
        questions_feedback = st.text_area(
            "Questions AI should have asked:",
            value=feedback.get('questions_feedback', ''),
            height=80,
            key="questions_feedback_sidebar",
            placeholder="List any missed questions...",
            label_visibility="collapsed"
        )
        
        if st.button("💾 Save", key="save_questions_sidebar", use_container_width=True):
            if api_client.save_conversation_feedback(
                doctor_name, conv['id'], questions_feedback=questions_feedback
            ):
                st.success("✅ Saved!")
                st.rerun()
    
    # Section 2: Duration Rating - collapsed by default
    with st.expander(f"⏱️ Duration {'✅' if has_duration_rating else '⏳'}", expanded=False):
        current_duration = feedback.get('duration_rating')
        
        if current_duration:
            st.caption(f"Current: **{current_duration}**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Short", key="dur_short_sb", use_container_width=True,
                        type="primary" if current_duration == "Too Short" else "secondary"):
                if api_client.save_conversation_feedback(doctor_name, conv['id'], duration_rating="Too Short"):
                    st.rerun()
        
        with col2:
            if st.button("Good", key="dur_optimal_sb", use_container_width=True,
                        type="primary" if current_duration == "Optimal" else "secondary"):
                if api_client.save_conversation_feedback(doctor_name, conv['id'], duration_rating="Optimal"):
                    st.rerun()
        
        with col3:
            if st.button("Long", key="dur_long_sb", use_container_width=True,
                        type="primary" if current_duration == "Too Long" else "secondary"):
                if api_client.save_conversation_feedback(doctor_name, conv['id'], duration_rating="Too Long"):
                    st.rerun()
    
    # Section 3: Overall Notes - collapsed by default
    with st.expander(f"💬 Overall Notes {'✅' if has_process_notes else '⏳'}", expanded=False):
        process_notes = st.text_area(
            "General feedback:",
            value=feedback.get('process_notes', ''),
            height=80,
            key="process_notes_sidebar",
            placeholder="Comments on flow, logic, experience...",
            label_visibility="collapsed"
        )
        
        if st.button("💾 Save", key="save_notes_sidebar", use_container_width=True):
            if api_client.save_conversation_feedback(doctor_name, conv['id'], process_notes=process_notes):
                st.success("✅ Saved!")
                st.rerun()


def render_diagnosis_section(conv):
    """Render the diagnosis section on the left side"""
    diagnosis_data = conv.get('final_diagnosis', {})
    ai_diagnosis = diagnosis_data.get('ai_diagnosis', '')
    
    st.markdown('<div class="section-header section-header-diagnosis">🩺 AI Diagnosis</div>', unsafe_allow_html=True)
    
    if ai_diagnosis:
        with st.container(height=500):
            st.markdown(ai_diagnosis)
    else:
        st.info("⏳ Diagnosis will appear here when ready")


def render_diagnosis_feedback(conv):
    """Render diagnosis feedback panel (right side, parallel to diagnosis)"""
    diagnosis_data = conv.get('final_diagnosis', {})
    api_client = get_api_client()
    doctor_name = get_session_state('doctor_name')
    
    has_diagnosis = bool(diagnosis_data.get('ai_diagnosis', ''))
    has_diagnosis_feedback = bool(diagnosis_data.get('diagnosis_feedback', '').strip())
    
    # Header
    st.markdown('<div class="section-header section-header-diagnosis">🩺 Diagnosis Feedback</div>', unsafe_allow_html=True)
    
    if not has_diagnosis:
        st.info("⏳ Waiting for diagnosis...")
        return
    
    if has_diagnosis_feedback:
        st.success("✅ Feedback Submitted")
    else:
        st.warning("⏳ Pending Feedback")
    
    diagnosis_feedback = st.text_area(
        "Your evaluation:",
        value=diagnosis_data.get('diagnosis_feedback', ''),
        height=180,
        key="diagnosis_feedback_sidebar",
        placeholder="""Evaluate:
• Diagnostic accuracy
• Clinical reasoning
• Completeness
• Recommendations quality
• What would you do differently?""",
        label_visibility="collapsed"
    )
    
    btn_text = "💾 Update Evaluation" if has_diagnosis_feedback else "💾 Save Evaluation"
    
    if st.button(btn_text, key="save_diag_sidebar", use_container_width=True, type="primary"):
        if api_client.save_diagnosis_feedback(doctor_name, conv['id'], diagnosis_feedback):
            st.success("✅ Saved!")
            st.rerun()


def conversation_detail_page():
    """Render the active conversation detail page"""
    
    doctor_name = get_session_state('doctor_name')
    active_id = get_session_state('active_conv_id')
    api_client = get_api_client()
    
    # Get conversation from API
    conv = api_client.get_conversation(doctor_name, active_id)
    
    if conv is None:
        st.error("Conversation not found.")
        if st.button("Back to Conversations"):
            set_session_state('current_page', 'conversation')
            st.rerun()
        return
    
    apply_chat_css()
    
    # Header
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        st.title(f"Conversation #{conv['id']}")
    with col2:
        if st.button("⬅️ Back", use_container_width=True):
            set_session_state('current_page', 'conversation')
            st.rerun()
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            clear_session()
            st.rerun()
    
    is_ended = conv.get('is_ended', False)
    
    # Check if diagnosis is available
    diagnosis_info = api_client.get_final_diagnosis(doctor_name, conv['id'])
    has_diagnosis = diagnosis_info.get('is_available', False) if diagnosis_info else False
    
    # Status banner
    if has_diagnosis and is_ended:
        st.markdown("""
        <div class="diagnosis-ready-banner">
            ✅ Final Diagnosis Ready
        </div>
        """, unsafe_allow_html=True)
    elif is_ended:
        st.markdown("""
        <div class="conversation-ended">
            🏁 Conversation Ended
        </div>
        """, unsafe_allow_html=True)
    else:
        # Get diagnostic status
        session_id = f"{doctor_name}_{conv['id']}"
        status = api_client.get_status(session_id)
        
        if status:
            questions_asked = status.get('questions_asked', 0)
            max_questions = status.get('max_allowed', 15)
            st.info(f"💬 Questions: {questions_asked}/{max_questions}")
    
    # ============================================
    # ROW 1: Chat (Left) | Conversation Feedback (Right)
    # ============================================
    chat_col, conv_feedback_col = st.columns([3, 2])
    
    # Left: Chat
    with chat_col:
        st.markdown("### 💬 Conversation")
        
        chat_height = 400 if has_diagnosis else 500
        messages_container = st.container(height=chat_height)
        
        with messages_container:
            if conv.get('messages') or st.session_state.get('pending_message'):
                for idx, msg in enumerate(conv.get('messages', [])):
                    if isinstance(msg, dict):
                        sender = msg['sender']
                        content = msg['content']
                    else:
                        sender, content = msg.split(': ', 1)
                    render_message(sender, content, idx, conv)
                
                # Display pending doctor message
                if st.session_state.get('pending_message'):
                    render_message("Doctor", st.session_state['pending_message'], None, None)
                
                # Display AI typing indicator
                if st.session_state.get('waiting_for_ai'):
                    st.markdown("""
                    <div class="message-container">
                        <div class="message ai-message">
                            <div class="typing-indicator">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Start the conversation by describing the patient's symptoms.")
        
        # Message input (only if not ended)
        if not is_ended:
            # Check if we're in "sending" mode
            if st.session_state.get('sending_message'):
                user_msg = st.session_state.get('pending_message')
                
                if user_msg:
                    session_id = f"{doctor_name}_{conv['id']}"
                    
                    api_response = api_client.send_message(
                        message=user_msg,
                        session_id=session_id,
                        doctor_name=doctor_name,
                        conversation_id=conv['id']
                    )
                    
                    st.session_state['sending_message'] = False
                    st.session_state['pending_message'] = None
                    st.session_state['waiting_for_ai'] = False
                    
                    if api_response:
                        if api_response.get('is_final_diagnosis'):
                            st.success("✅ Final diagnosis generated!")
                        st.rerun()
                    else:
                        st.error("Failed to get response.")
                        st.rerun()
            
            # Message input form
            with st.form("message_form", clear_on_submit=True):
                cols = st.columns([8, 2])
                
                with cols[0]:
                    user_msg = st.text_input(
                        "Type your message:",
                        placeholder="Describe symptoms or answer...",
                        label_visibility="collapsed"
                    )
                
                with cols[1]:
                    send = st.form_submit_button("📤 Send", type="primary", use_container_width=True)
            
            if send and user_msg:
                health = api_client.health_check()
                if health.get("status") != "healthy":
                    st.error("⚠️ Backend unavailable!")
                    st.stop()
                
                st.session_state['pending_message'] = user_msg
                st.session_state['waiting_for_ai'] = True
                st.session_state['sending_message'] = True
                st.rerun()
    
    # Right: Conversation Feedback
    with conv_feedback_col:
        render_conversation_feedback(conv)
    
    # ============================================
    # ROW 2: Diagnosis (Left) | Diagnosis Feedback (Right)
    # ============================================
    if has_diagnosis or is_ended:
        st.markdown("---")
        
        diag_col, diag_feedback_col = st.columns([3, 2])
        
        # Left: Diagnosis
        with diag_col:
            render_diagnosis_section(conv)
        
        # Right: Diagnosis Feedback
        with diag_feedback_col:
            render_diagnosis_feedback(conv)
    
    # Refresh button at bottom
    st.markdown("---")
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
