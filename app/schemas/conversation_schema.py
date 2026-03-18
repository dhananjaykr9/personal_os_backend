from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

class ConversationBase(BaseModel):
    role: str
    content: str
    metadata_json: Optional[Dict[str, Any]] = None

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: UUID
    timestamp: datetime

    class Config:
        orm_mode = True

class OrinRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class OrinResponse(BaseModel):
    response: str
    actions: List[Dict[str, Any]] = []
