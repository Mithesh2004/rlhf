from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Literal, Optional
import sys
sys.path.append('..')

from services.chatbot_service import ChatbotService
from database.operations import ConversationOperations

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: str
    doctor_name: str
    conversation_id: int


class ChatResponse(BaseModel):
    response: str
    session_id: str
    response_type: Literal["question", "diagnosis"]
    is_final_diagnosis: bool
    final_diagnosis: Optional[str] = None  # Separate field for diagnosis
    conversation_state: Dict


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send message to AI chatbot"""
    try:
        chatbot = ChatbotService.get_instance()
        
        # Generate session ID
        session_id = f"{request.doctor_name}_{request.conversation_id}"
        
        # Get conversation to retrieve patient demographics
        conversation = ConversationOperations.get_conversation(
            request.doctor_name,
            request.conversation_id
        )
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        patient_age = conversation.get("patient_age")
        patient_gender = conversation.get("patient_gender")
        
        # Get AI response with patient demographics
        ai_response = chatbot.chat(
            request.message, 
            session_id=session_id,
            patient_age=patient_age,
            patient_gender=patient_gender
        )
        
        response_type = ai_response.get("type", "question")
        response_content = ai_response.get("content", "")
        
        # Add doctor message to database
        ConversationOperations.add_message(
            request.doctor_name,
            request.conversation_id,
            "Doctor",
            request.message
        )
        
        # Check if this is a diagnosis
        is_final = (response_type == "diagnosis")
        final_diagnosis = None
        
        if is_final:
            # Don't add diagnosis to chat messages
            # Instead, save it separately
            final_diagnosis = response_content
            
            # Save diagnosis to final_diagnosis field
            ConversationOperations.update_diagnosis(
                request.doctor_name,
                request.conversation_id,
                response_content
            )
            
            # Add a system message to chat indicating diagnosis is ready
            system_msg = "✅ Final diagnosis has been generated. Please review it in the Diagnosis tab below."
            ConversationOperations.add_message(
                request.doctor_name,
                request.conversation_id,
                "System",
                system_msg
            )
            
            # End conversation
            ConversationOperations.end_conversation(
                request.doctor_name,
                request.conversation_id
            )
            
            # Return system message as response, not the diagnosis
            response_content = system_msg
        else:
            # Add question to chat messages
            ConversationOperations.add_message(
                request.doctor_name,
                request.conversation_id,
                "AI",
                response_content
            )
        
        # Get conversation state
        state = chatbot.get_diagnostic_summary(session_id)
        
        return ChatResponse(
            response=response_content,
            session_id=session_id,
            response_type=response_type,
            is_final_diagnosis=is_final,
            final_diagnosis=final_diagnosis,
            conversation_state=state
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.post("/reset")
async def reset_session(session_id: str):
    """Reset chat session"""
    try:
        chatbot = ChatbotService.get_instance()
        chatbot.reset_session(session_id)
        return {"message": "Session reset successfully", "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{session_id}")
async def get_status(session_id: str):
    """Get diagnostic status"""
    try:
        chatbot = ChatbotService.get_instance()
        chatbot.set_session(session_id)
        summary = chatbot.get_diagnostic_summary(session_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diagnosis/{doctor_name}/{conversation_id}")
async def get_final_diagnosis(doctor_name: str, conversation_id: int):
    """Get the final diagnosis for a conversation"""
    try:
        conversation = ConversationOperations.get_conversation(doctor_name, conversation_id)
        
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        final_diagnosis = conversation.get("final_diagnosis", {}).get("ai_diagnosis", "")
        is_ended = conversation.get("is_ended", False)
        
        return {
            "diagnosis": final_diagnosis,
            "is_available": bool(final_diagnosis),
            "is_ended": is_ended
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
