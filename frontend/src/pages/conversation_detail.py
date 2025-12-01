import streamlit as st
from ..utils.session_state import get_session_state, set_session_state, clear_session
from ..utils.api_client import get_api_client


def apply_chat_css():
    """Apply custom CSS for chat interface"""
    st.markdown("""
    <style>
    .chat-container {
        margin-bottom: 20px;
        clear: both;
        overflow: hidden;
    }
    .message {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 75%;
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
        padding: 15px;
        margin: 20px 0;
        text-align: center;
    }
    .diagnosis-ready-banner {
        background-color: #d4edda;
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        text-align: center;
        font-size: 16px;
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
        # Escape HTML and preserve newlines
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
            
            # Count total AI messages for priority range
            total_ai_messages = count_ai_messages(conv.get('messages', []))
            
            # Get all assigned priorities
            assigned_priorities = set()
            for msg in conv.get('messages', []):
                if isinstance(msg, dict) and msg.get('sender') == 'AI':
                    if msg.get('priority') is not None:
                        assigned_priorities.add(msg.get('priority'))
            
            col1, col2, col3 = st.columns([1, 1, 6])
            
            with col1:
                if st.button("👍🏼", key=f"relevant_{message_index}",
                           help="Relevant", use_container_width=True,
                           type="primary" if current_rating == "relevant" else "secondary"):
                    if api_client.update_message_rating(doctor_name, conv['id'], message_index, "relevant"):
                        st.rerun()
            
            with col2:
                if st.button("👎🏼", key=f"irrelevant_{message_index}",
                           help="Irrelevant/Wrong Direction", use_container_width=True,
                           type="primary" if current_rating == "irrelevant" else "secondary"):
                    if api_client.update_message_rating(doctor_name, conv['id'], message_index, "irrelevant"):
                        st.rerun()
                    
            with col3:
                # Priority selector with popover
                if current_priority is not None:
                    button_label = f"⭐ Priority: {current_priority}"
                else:
                    button_label = "⚠️ Set Priority"
                
                with st.popover(button_label, use_container_width=False):
                    st.markdown("**Set Priority Rank**")
                    st.caption(f"Rank 1 = Highest Priority, Rank {total_ai_messages} = Lowest Priority")
                    
                    for row_start in range(1, total_ai_messages + 1, 5):
                        cols = st.columns(min(5, total_ai_messages - row_start + 1))
                        for i, col in enumerate(cols):
                            priority_num = row_start + i
                            if priority_num <= total_ai_messages:
                                with col:
                                    is_assigned = priority_num in assigned_priorities and current_priority != priority_num
                                    is_current = current_priority == priority_num
                                    
                                    button_type = "primary" if is_current else "secondary"
                                    disabled = is_assigned
                                    
                                    button_label_text = str(priority_num)
                                    if is_assigned:
                                        button_label_text += " ✓"
                                    
                                    if st.button(
                                        button_label_text,
                                        key=f"priority_{priority_num}_{message_index}",
                                        use_container_width=True,
                                        type=button_type,
                                        disabled=disabled,
                                        help="Already assigned" if is_assigned else f"Set priority rank {priority_num}"
                                    ):
                                        if api_client.update_message_priority(doctor_name, conv['id'], message_index, priority_num):
                                            st.rerun()
                    
                    if current_priority is not None:
                        st.divider()
                        if st.button("❌ Clear Priority", key=f"clear_{message_index}",
                                   use_container_width=True):
                            if api_client.update_message_priority(doctor_name, conv['id'], message_index, 0):
                                st.rerun()


def render_final_diagnosis(conv):
    """Render the AI-generated final diagnosis with feedback form"""
    st.markdown("---")
    st.markdown("## 🩺 AI-Generated Final Diagnosis")
    
    diagnosis_data = conv.get('final_diagnosis', {})
    ai_diagnosis = diagnosis_data.get('ai_diagnosis', '')
    
    if ai_diagnosis:
        st.markdown("### Diagnosis Report")
        
        # Display the diagnosis in markdown format
        st.markdown(ai_diagnosis)
        
        st.markdown("---")
        
    else:
        st.info("⏳ Waiting for AI to generate final diagnosis...")
        st.caption("The AI will automatically provide a diagnosis when sufficient information is gathered.")
        return
    
    # Feedback section with indicator
    existing_feedback = diagnosis_data.get('diagnosis_feedback', '')
    has_feedback = bool(existing_feedback and existing_feedback.strip())
    
    # Header with status badge
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📝 Provide Your Expert Evaluation")
    with col2:
        if has_feedback:
            st.markdown("""
            <div style="background-color: #d4edda; color: #155724; padding: 8px 12px; 
                        border-radius: 20px; text-align: center; font-weight: 500; 
                        border: 1px solid #c3e6cb; margin-top: 5px;">
                ✅ Submitted
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #fff3cd; color: #856404; padding: 8px 12px; 
                        border-radius: 20px; text-align: center; font-weight: 500; 
                        border: 1px solid #ffeeba; margin-top: 5px;">
                ⏳ Pending
            </div>
            """, unsafe_allow_html=True)
    
    diagnosis_feedback = st.text_area(
        "Your Professional Assessment:",
        value=existing_feedback,
        height=300,
        key="diagnosis_feedback_input",
        placeholder="""Please provide detailed feedback on:

**Diagnostic Accuracy**
• Primary diagnosis correctness
• Appropriateness of differential diagnoses
• Accuracy of confidence levels

**Clinical Reasoning**
• Soundness of diagnostic logic
• Proper consideration of symptoms
• Evidence-based approach

**Completeness**
• Coverage of relevant conditions
• Thoroughness of evaluation
• Missing considerations

**Recommendations Quality**
• Appropriateness of suggested actions
• Relevance of tests/evaluations
• Accuracy of urgency assessment
• Correct department referral

**Overall Assessment**
• Agreement with diagnosis
• What would you do differently?
• Suggestions for improvement
• Training opportunities identified"""
    )
    
    button_text = "💾 Update Diagnosis Evaluation" if has_feedback else "💾 Save Diagnosis Evaluation"
    
    if st.button(button_text, type="primary", key="save_diagnosis_feedback"):
        api_client = get_api_client()
        doctor_name = get_session_state('doctor_name')
        
        if api_client.save_diagnosis_feedback(doctor_name, conv['id'], diagnosis_feedback):
            st.success("✅ Your evaluation has been saved successfully!")
            st.rerun()
        else:
            st.error("Failed to save evaluation. Please try again.")


def render_holistic_feedback(conv):
    """Render the holistic RLHF feedback form"""
    st.markdown("---")
    st.markdown("## 💬 Conversation Quality Feedback")
    
    feedback = conv.get('holistic_feedback', {})
    api_client = get_api_client()
    doctor_name = get_session_state('doctor_name')
    
    # Check what feedback exists
    has_questions_feedback = bool(feedback.get('questions_feedback', '').strip())
    has_duration_rating = bool(feedback.get('duration_rating'))
    has_process_notes = bool(feedback.get('process_notes', '').strip())
    
    # Section 1: Questions Quality
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📋 AI Questions Assessment")
    with col2:
        if has_questions_feedback:
            st.markdown("""
            <div style="background-color: #d4edda; color: #155724; padding: 6px 10px; 
                        border-radius: 15px; text-align: center; font-size: 13px;
                        font-weight: 500; border: 1px solid #c3e6cb; margin-top: 8px;">
                ✅ Done
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #fff3cd; color: #856404; padding: 6px 10px; 
                        border-radius: 15px; text-align: center; font-size: 13px;
                        font-weight: 500; border: 1px solid #ffeeba; margin-top: 8px;">
                ⏳ Pending
            </div>
            """, unsafe_allow_html=True)
    
    questions_feedback = st.text_area(
        "Enter the missed questions:",
        value=feedback.get('questions_feedback', ''),
        height=200,
        key="questions_feedback_input",
        placeholder="""Mention the specific questions the AI should have asked but didn't (if any)"""
    )
    
    button_text = "💾 Update Questions Feedback" if has_questions_feedback else "💾 Save Questions Feedback"
    
    if st.button(button_text, type="secondary", key="save_questions_feedback"):
        if api_client.save_conversation_feedback(
            doctor_name, conv['id'], questions_feedback=questions_feedback
        ):
            st.success("✅ Questions feedback saved!")
            st.rerun()
    
    # Section 2: Duration Rating
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### ⏱️ Conversation Length")
    with col2:
        if has_duration_rating:
            st.markdown("""
            <div style="background-color: #d4edda; color: #155724; padding: 6px 10px; 
                        border-radius: 15px; text-align: center; font-size: 13px;
                        font-weight: 500; border: 1px solid #c3e6cb; margin-top: 8px;">
                ✅ Done
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #fff3cd; color: #856404; padding: 6px 10px; 
                        border-radius: 15px; text-align: center; font-size: 13px;
                        font-weight: 500; border: 1px solid #ffeeba; margin-top: 8px;">
                ⏳ Pending
            </div>
            """, unsafe_allow_html=True)
    
    current_duration = feedback.get('duration_rating')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Too Long", key="duration_too_long", 
                   use_container_width=True,
                   type="primary" if current_duration == "Too Long" else "secondary"):
            if api_client.save_conversation_feedback(doctor_name, conv['id'], duration_rating="Too Long"):
                st.success("✅ Duration rating saved!")
                st.rerun()
    
    with col2:
        if st.button("Optimal", key="duration_optimal",
                   use_container_width=True,
                   type="primary" if current_duration == "Optimal" else "secondary"):
            if api_client.save_conversation_feedback(doctor_name, conv['id'], duration_rating="Optimal"):
                st.success("✅ Duration rating saved!")
                st.rerun()
    
    with col3:
        if st.button("Too Short", key="duration_too_short",
                   use_container_width=True,
                   type="primary" if current_duration == "Too Short" else "secondary"):
            if api_client.save_conversation_feedback(doctor_name, conv['id'], duration_rating="Too Short"):
                st.success("✅ Duration rating saved!")
                st.rerun()
    
    # Show selected duration
    if current_duration:
        st.info(f"📊 Current rating: **{current_duration}**")
    
    # Section 3: General Process Notes
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📝 Overall Experience")
    with col2:
        if has_process_notes:
            st.markdown("""
            <div style="background-color: #d4edda; color: #155724; padding: 6px 10px; 
                        border-radius: 15px; text-align: center; font-size: 13px;
                        font-weight: 500; border: 1px solid #c3e6cb; margin-top: 8px;">
                ✅ Done
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #fff3cd; color: #856404; padding: 6px 10px; 
                        border-radius: 15px; text-align: center; font-size: 13px;
                        font-weight: 500; border: 1px solid #ffeeba; margin-top: 8px;">
                ⏳ Pending
            </div>
            """, unsafe_allow_html=True)
    
    process_notes = st.text_area(
        "General feedback:",
        value=feedback.get('process_notes', ''),
        height=150,
        key="process_notes_input",
        placeholder="Comments on flow, logic, style, and overall experience..."
    )
    
    button_text = "💾 Update Overall Feedback" if has_process_notes else "💾 Save Overall Feedback"
    
    if st.button(button_text, type="primary", key="save_holistic_feedback"):
        if api_client.save_conversation_feedback(doctor_name, conv['id'], process_notes=process_notes):
            st.success("✅ Overall feedback saved!")
            st.rerun()
    
    # Overall completion status
    st.markdown("---")
    completed_count = sum([has_questions_feedback, has_duration_rating, has_process_notes])
    total_count = 3
    
    if completed_count == total_count:
        st.success(f"🎉 All feedback completed ({completed_count}/{total_count})")
    else:
        st.info(f"📊 Feedback progress: {completed_count}/{total_count} sections completed")


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
    
    st.title(f"Conversation #{conv['id']} - Dr. {doctor_name}")
    
    apply_chat_css()
    
    is_ended = conv.get('is_ended', False)
    
    # Check if diagnosis is available
    diagnosis_info = api_client.get_final_diagnosis(doctor_name, conv['id'])
    has_diagnosis = diagnosis_info.get('is_available', False) if diagnosis_info else False
    
    # Display status banner
    if has_diagnosis and is_ended:
        st.markdown("""
        <div class="diagnosis-ready-banner">
            ✅ Final Diagnosis Ready - Review it in the "AI Diagnosis & Feedback" tab below
        </div>
        """, unsafe_allow_html=True)
    elif is_ended:
        st.markdown("""
        <div class="conversation-ended">
            <h3>🏁 Conversation Ended</h3>
            <p>Please provide your feedback below.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Get diagnostic status
        session_id = f"{doctor_name}_{conv['id']}"
        status = api_client.get_status(session_id)
        
        if status:
            questions_asked = status.get('questions_asked', 0)
            min_required = status.get('min_required', 5)
            max_questions = status.get('max_allowed', 15)
            
            progress_text = f"💬 Questions: {questions_asked}/{max_questions}"
            if questions_asked < min_required:
                progress_text += f" (min {min_required} for diagnosis)"
            
            st.info(progress_text)
            
            aspects = status.get('aspects_covered', [])
            if aspects:
                st.caption(f"📊 Covered: {', '.join(aspects)}")
    
    # Messages area
    st.markdown("### Conversation")
    
    # Create a container for messages
    messages_container = st.container()
    
    with messages_container:
        if conv.get('messages') or st.session_state.get('pending_message'):
            # Display existing messages
            for idx, msg in enumerate(conv.get('messages', [])):
                if isinstance(msg, dict):
                    sender = msg['sender']
                    content = msg['content']
                else:
                    sender, content = msg.split(': ', 1)
                render_message(sender, content, idx, conv)
            
            # Display pending doctor message (optimistic update)
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
    
    # Show tabs only if conversation is ended
    if is_ended:
        tab1, tab2 = st.tabs(["🩺 AI Diagnosis & Feedback", "💬 Conversation Feedback"])
        
        with tab1:
            render_final_diagnosis(conv)
        
        with tab2:
            render_holistic_feedback(conv)
    else:
        # Check if we're in "sending" mode
        if st.session_state.get('sending_message'):
            # We're processing a message - show it and call API
            user_msg = st.session_state.get('pending_message')
            
            if user_msg:
                session_id = f"{doctor_name}_{conv['id']}"
                
                # Call API
                api_response = api_client.send_message(
                    message=user_msg,
                    session_id=session_id,
                    doctor_name=doctor_name,
                    conversation_id=conv['id']
                )
                
                # Clear sending state
                st.session_state['sending_message'] = False
                st.session_state['pending_message'] = None
                st.session_state['waiting_for_ai'] = False
                
                if api_response:
                    if api_response.get('is_final_diagnosis'):
                        st.success("✅ Final diagnosis generated! Check the tabs below.")
                    else:
                        st.success("✅ Response received!")
                    st.rerun()
                else:
                    st.error("Failed to get response. Please try again.")
                    st.rerun()
        
        # Message input (only if not ended)
        st.markdown("---")
        
        # Use form for Enter key submission
        with st.form("message_form", clear_on_submit=True):
            cols = st.columns([8, 2])
            
            with cols[0]:
                user_msg = st.text_input(
                    "Type your message:",
                    placeholder="Describe symptoms or answer AI's question...",
                    label_visibility="collapsed"
                )
            
            with cols[1]:
                send = st.form_submit_button("📤 Send", type="primary", use_container_width=True)
        
        if send and user_msg:
            # Check AI health
            health = api_client.health_check()
            if health.get("status") != "healthy":
                st.error("⚠️ Backend service unavailable!")
                st.stop()
            
            # Set pending state and trigger rerun to show message
            st.session_state['pending_message'] = user_msg
            st.session_state['waiting_for_ai'] = True
            st.session_state['sending_message'] = True
            
            # This rerun will show the message and typing indicator
            # Then the code above will handle the API call
            st.rerun()
    
    # Controls
    st.markdown("---")
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("🚪 Logout", use_container_width=True):
            clear_session()
            st.rerun()
    with cols[1]:
        if st.button("⬅️ Back to Conversations", use_container_width=True):
            set_session_state('current_page', 'conversation')
            st.rerun()
    with cols[2]:
        if st.button("🔄 Refresh", type="primary", use_container_width=True):
            st.rerun()
