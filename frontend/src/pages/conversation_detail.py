import streamlit as st
from ..utils.session_state import get_session_state, set_session_state
from ..utils.conversation_manager import add_message, save_conversations


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
        color: #666;
        font-style: italic;
    }
    .timestamp {
        font-size: 0.8em;
        color: #666;
        margin-top: 5px;
    }
    .rating-container {
        margin-top: 0;
        display: flex;
        gap: 5px;
        padding-left: 10px;
        align-items: center;
    }
    .rating-button {
        display: inline-block;
    }
    .rating-button button {
        background: none;
        border: none;
        padding: 0;
        font-size: 1.2em;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.2s;
    }
    .rating-button button:hover {
        opacity: 1;
    }
    .rating-button button.selected {
        opacity: 1;
        color: #007AFF;
    }
    .priority-label {
        font-size: 0.9em;
        padding: 4px 8px;
        border-radius: 4px;
        background: #f0f0f0;
        color: #333;
        font-weight: 500;
    }
    .priority-high {
        background: #ffebee;
        color: #c62828;
    }
    .priority-medium {
        background: #fff3e0;
        color: #ef6c00;
    }
    .priority-low {
        background: #e8f5e9;
        color: #2e7d32;
    }
    .conversation-ended {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


def count_ai_messages(messages):
    """Count the number of AI messages in the conversation"""
    count = 0
    for msg in messages:
        if isinstance(msg, dict):
            if msg.get('sender') == 'AI':
                count += 1
        else:
            if msg.startswith('AI: '):
                count += 1
    return count


def render_message(sender, content, message_index=None):
    """Render a chat message with the appropriate styling"""
    if sender == "System":
        st.markdown(f'<div class="system-message">{content}</div>', unsafe_allow_html=True)
    else:
        css_class = "doctor-message" if sender == "Doctor" else "ai-message"
        st.markdown(f"""
        <div class="message-container">
            <div class="message {css_class}">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add rating and priority buttons only for AI messages
        if sender == "AI" and message_index is not None:
            conversations = get_session_state('conversations')
            active_id = get_session_state('active_conv_id')
            current_conv = next((c for c in conversations if c['id'] == active_id), None)
            
            if current_conv:
                # Get current rating and priority from message if it exists
                message_data = current_conv['messages'][message_index]
                if isinstance(message_data, dict):
                    current_rating = message_data.get('rating')
                    current_priority = message_data.get('priority')
                else:
                    # Convert string message to dict if needed
                    current_conv['messages'][message_index] = {
                        'content': message_data,
                        'sender': sender,
                        'rating': None,
                        'priority': None
                    }
                    current_rating = None
                    current_priority = None
                
                col1, col2, col3 = st.columns([1, 1, 6])
                
                with col1:
                    if st.button("👍🏼", key=f"relevant_{message_index}",
                               help="Relevant", use_container_width=True,
                               type="primary" if current_rating == "relevant" else "secondary"):
                        current_conv['messages'][message_index]['rating'] = "relevant"
                        save_conversations(conversations)
                        st.rerun()
                
                with col2:
                    if st.button("👎🏼", key=f"irrelevant_{message_index}",
                               help="Irrelevant/Wrong Direction", use_container_width=True,
                               type="primary" if current_rating == "irrelevant" else "secondary"):
                        current_conv['messages'][message_index]['rating'] = "irrelevant"
                        save_conversations(conversations)
                        st.rerun()
                        
                with col3:
                    # Priority selector with popover
                    priority_display = {
                        'high': ('🔴 High Priority', 'priority-high'),
                        'medium': ('🟡 Medium Priority', 'priority-medium'),
                        'low': ('🟢 Low Priority', 'priority-low')
                    }
                    
                    # Create a popover for priority selection
                    if current_priority:
                        label, css_class = priority_display[current_priority]
                        button_label = label
                    else:
                        button_label = "⚠️ Set Priority"
                        css_class = ""
                    
                    with st.popover(button_label, use_container_width=False):
                        st.markdown("**Set Priority**")
                        
                        if st.button("🔴 High Priority", key=f"high_{message_index}", 
                                   use_container_width=True,
                                   type="primary" if current_priority == "high" else "secondary"):
                            current_conv['messages'][message_index]['priority'] = "high"
                            save_conversations(conversations)
                            st.rerun()
                        
                        if st.button("🟡 Medium Priority", key=f"medium_{message_index}",
                                   use_container_width=True,
                                   type="primary" if current_priority == "medium" else "secondary"):
                            current_conv['messages'][message_index]['priority'] = "medium"
                            save_conversations(conversations)
                            st.rerun()
                        
                        if st.button("🟢 Low Priority", key=f"low_{message_index}",
                                   use_container_width=True,
                                   type="primary" if current_priority == "low" else "secondary"):
                            current_conv['messages'][message_index]['priority'] = "low"
                            save_conversations(conversations)
                            st.rerun()
                        
                        # Add option to clear priority if one is set
                        if current_priority:
                            st.divider()
                            if st.button("❌ Clear Priority", key=f"clear_{message_index}",
                                       use_container_width=True):
                                current_conv['messages'][message_index]['priority'] = None
                                save_conversations(conversations)
                                st.rerun()


def render_holistic_feedback(conv):
    """Render the holistic RLHF feedback form after conversation completion"""
    st.markdown("---")
    st.markdown("## Feedback")
    
    # Get existing feedback or initialize
    feedback = conv.get('holistic_feedback', {
        'duration_rating': None,
        'process_notes': ''
    })
    
    # F-3.3.1: Duration/Length Rating
    st.markdown("### Duration Rating")
    st.markdown("Rate the overall length of the conversation:")
    
    duration_options = ["Too Long", "Optimal", "Too Short"]
    current_duration = feedback.get('duration_rating')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Too Long", key="duration_too_long", 
                   use_container_width=True,
                   type="primary" if current_duration == "Too Long" else "secondary"):
            feedback['duration_rating'] = "Too Long"
            conv['holistic_feedback'] = feedback
            conversations = get_session_state('conversations')
            save_conversations(conversations)
            st.rerun()
    
    with col2:
        if st.button("Optimal", key="duration_optimal",
                   use_container_width=True,
                   type="primary" if current_duration == "Optimal" else "secondary"):
            feedback['duration_rating'] = "Optimal"
            conv['holistic_feedback'] = feedback
            conversations = get_session_state('conversations')
            save_conversations(conversations)
            st.rerun()
    
    with col3:
        if st.button("Too Short", key="duration_too_short",
                   use_container_width=True,
                   type="primary" if current_duration == "Too Short" else "secondary"):
            feedback['duration_rating'] = "Too Short"
            conv['holistic_feedback'] = feedback
            conversations = get_session_state('conversations')
            save_conversations(conversations)
            st.rerun()
    
    # F-3.3.2: General Process Notes
    st.markdown("### General Process Notes")
    st.markdown("Provide general qualitative feedback on the flow, logic, and style of the conversation:")
    
    process_notes = st.text_area(
        "Your feedback:",
        value=feedback.get('process_notes', ''),
        height=150,
        key="process_notes_input",
        placeholder="Share your thoughts on the conversation flow, AI's logic, questioning style, and overall experience..."
    )
    
    if st.button("Save Feedback", type="primary", key="save_holistic_feedback"):
        feedback['process_notes'] = process_notes
        conv['holistic_feedback'] = feedback
        conversations = get_session_state('conversations')
        save_conversations(conversations)
        st.success("Feedback saved successfully!")
        st.rerun()


def conversation_detail_page():
    """Render the active conversation detail page where doctor and AI exchange messages."""
    doctor_name = get_session_state('doctor_name')
    active_id = get_session_state('active_conv_id')
    conversations = get_session_state('conversations') or []

    # Find the active conversation for THIS doctor
    conv = None
    for c in conversations:
        if c.get('id') == active_id and c.get('doctor') == doctor_name:
            conv = c
            break

    if conv is None:
        st.error("Active conversation not found for this doctor.")
        if st.button("Back to Conversations"):
            set_session_state('current_page', 'conversation')
            st.rerun()
        return

    st.title(f"Conversation #{conv['id']} - Dr. {doctor_name}")
    
    # Apply custom CSS for chat interface
    apply_chat_css()
    
    # Check if conversation is ended
    is_ended = conv.get('is_ended', False)
    
    # If this is the first time viewing the conversation, send the initial problem and get AI response
    if not conv.get('messages'):
        initial_message = f"Initial Patient Problem: {conv.get('initial_problem', 'No initial problem specified')}"
        add_message(conv['id'], 'Doctor', initial_message)
        # Add initial AI response
        ai_initial_reply = "Thank you for providing the patient's problem. I'll help you analyze this case. What additional symptoms or medical history should we consider?"
        add_message(conv['id'], 'AI', ai_initial_reply)
        st.rerun()
    
    # Count AI messages
    ai_message_count = count_ai_messages(conv.get('messages', []))
    
    # Display conversation status
    if is_ended:
        st.markdown(f"""
        <div class="conversation-ended">
            <h3>🏁 Conversation Ended</h3>
            <p>This conversation has been completed after {ai_message_count} AI responses.</p>
            <p>Please provide your feedback below.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        remaining = 5 - ai_message_count
        if remaining > 0:
            st.info(f"💬 AI responses: {ai_message_count}")
    
    # Messages area
    st.markdown("### Messages")
    if conv.get('messages'):
        for idx, msg in enumerate(conv.get('messages', [])):
            if isinstance(msg, dict):
                sender = msg['sender']
                content = msg['content']
            else:
                # Handle old message format
                sender, content = msg.split(': ', 1)
            render_message(sender, content, idx)
    else:
        st.info("No messages yet. Send the first message below.")

    # Show holistic feedback form if conversation is ended
    if is_ended:
        render_holistic_feedback(conv)
    else:
        # Message input area with custom styling (only if not ended)
        st.markdown("""
            <style>
            .stTextInput input {
                border-radius: 20px;
                padding: 10px 15px;
                border: 1px solid #ccc;
            }
            .stButton > button {
                border-radius: 20px;
                padding: 10px 25px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Create a row with message input and send button
        cols = st.columns([8, 2])
        
        with cols[0]:
            user_msg = st.text_input("Type your message...", key="user_msg_input")
        with cols[1]:
            send = st.button("Send", type="primary")

        if send and user_msg:
            # Add doctor's message as a dictionary
            conversations = get_session_state('conversations')
            # Find the conversation for THIS doctor
            conv = next((c for c in conversations if c['id'] == active_id and c.get('doctor') == doctor_name), None)
            if conv:
                conv['messages'].append({
                    'sender': 'Doctor',
                    'content': user_msg,
                    'rating': None,
                    'priority': None
                })
                
                # Check if we've reached 5 AI messages
                current_ai_count = count_ai_messages(conv['messages'])
                
                if current_ai_count < 5:
                    # Add AI response (placeholder)
                    ai_reply = f"AI response #{current_ai_count + 1}"
                    conv['messages'].append({
                        'sender': 'AI',
                        'content': ai_reply,
                        'rating': None,
                        'priority': None
                    })
                    
                    # Check if this was the 5th AI message
                    if current_ai_count + 1 >= 5:
                        conv['is_ended'] = True
                        conv['messages'].append({
                            'sender': 'System',
                            'content': '🏁 Conversation has ended after 5 AI responses. Please provide your feedback below.',
                            'rating': None,
                            'priority': None
                        })
                
                save_conversations(conversations)
                st.rerun()

    # Controls
    st.markdown("---")
    cols = st.columns([1, 1])  # Two columns for End Session and Save & Close
    with cols[0]:
        if st.button("End Session"):
            set_session_state('doctor_name', None)
            set_session_state('current_page', 'login')
            st.rerun()
    with cols[1]:
        if st.button("Save & Close", type="primary"):
            save_conversations(conversations)
            st.success("Conversation saved successfully!")
            set_session_state('current_page', 'conversation')
            st.rerun()
