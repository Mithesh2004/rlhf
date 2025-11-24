from fastapi import APIRouter, HTTPException
from typing import List
import sys
sys.path.append('..')

from models.conversation import ConversationCreate, MessageAdd
from database.operations import ConversationOperations

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/create")
async def create_conversation(request: ConversationCreate):
    """Create a new conversation"""
    try:
        conversation = ConversationOperations.create_conversation(
            request.doctor_name,
            request.initial_problem
        )
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{doctor_name}")
async def get_doctor_conversations(doctor_name: str):
    """Get all conversations for a doctor"""
    try:
        conversations = ConversationOperations.get_doctor_conversations(doctor_name)
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{doctor_name}/{conversation_id}")
async def get_conversation(doctor_name: str, conversation_id: int):
    """Get a specific conversation"""
    try:
        conversation = ConversationOperations.get_conversation(doctor_name, conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message/add")
async def add_message(request: MessageAdd):
    """Add a message to conversation"""
    try:
        success = ConversationOperations.add_message(
            request.doctor_name,
            request.conversation_id,
            request.sender,
            request.content
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/end")
async def end_conversation(doctor_name: str, conversation_id: int):
    """Mark conversation as ended"""
    try:
        success = ConversationOperations.end_conversation(doctor_name, conversation_id)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
