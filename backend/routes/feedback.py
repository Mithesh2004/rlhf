from fastapi import APIRouter, HTTPException
import sys
sys.path.append('..')

from models.feedback import (
    MessageRating,
    MessagePriority,
    DiagnosisFeedback,
    ConversationFeedback
)
from database.operations import ConversationOperations

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/message/rating")
async def update_message_rating(request: MessageRating):
    """Update message rating"""
    try:
        success = ConversationOperations.update_message_rating(
            request.doctor_name,
            request.conversation_id,
            request.message_index,
            request.rating
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message/priority")
async def update_message_priority(request: MessagePriority):
    """Update message priority"""
    try:
        success = ConversationOperations.update_message_priority(
            request.doctor_name,
            request.conversation_id,
            request.message_index,
            request.priority
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/diagnosis")
async def save_diagnosis_feedback(request: DiagnosisFeedback):
    """Save diagnosis feedback"""
    try:
        success = ConversationOperations.save_diagnosis_feedback(
            request.doctor_name,
            request.conversation_id,
            request.diagnosis_feedback
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversation")
async def save_conversation_feedback(request: ConversationFeedback):
    """Save conversation feedback"""
    try:
        success = ConversationOperations.save_conversation_feedback(
            request.doctor_name,
            request.conversation_id,
            request.questions_feedback,
            request.duration_rating,
            request.process_notes
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
