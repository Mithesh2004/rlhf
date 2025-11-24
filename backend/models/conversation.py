from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class Message(BaseModel):
    sender: str
    content: str
    rating: Optional[str] = None
    priority: Optional[int] = None


class HolisticFeedback(BaseModel):
    duration_rating: Optional[str] = None
    process_notes: str = ""
    questions_feedback: str = ""


class FinalDiagnosis(BaseModel):
    ai_diagnosis: str = ""
    diagnosis_feedback: str = ""


class Conversation(BaseModel):
    id: int
    timestamp: str
    doctor: str
    initial_problem: str
    messages: List[Message] = []
    is_ended: bool = False
    holistic_feedback: HolisticFeedback
    final_diagnosis: FinalDiagnosis


class ConversationCreate(BaseModel):
    doctor_name: str
    initial_problem: str


class MessageAdd(BaseModel):
    doctor_name: str
    conversation_id: int
    sender: str
    content: str
