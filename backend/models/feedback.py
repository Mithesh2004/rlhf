from pydantic import BaseModel
from typing import Optional


class MessageRating(BaseModel):
    doctor_name: str
    conversation_id: int
    message_index: int
    rating: str  # "relevant" or "irrelevant"


class MessagePriority(BaseModel):
    doctor_name: str
    conversation_id: int
    message_index: int
    priority: int


class DiagnosisFeedback(BaseModel):
    doctor_name: str
    conversation_id: int
    diagnosis_feedback: str


class ConversationFeedback(BaseModel):
    doctor_name: str
    conversation_id: int
    questions_feedback: Optional[str] = None
    duration_rating: Optional[str] = None
    process_notes: Optional[str] = None
