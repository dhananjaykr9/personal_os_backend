from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class LearningLogBase(BaseModel):
    topic_name: str
    topic_id: Optional[UUID] = None
    hours_studied: Optional[float] = 0.0
    what_learned: Optional[str] = None
    difficulty: Optional[str] = "medium"
    log_date: Optional[date] = None

class LearningLogCreate(LearningLogBase):
    pass

class LearningLogUpdate(BaseModel):
    topic_name: Optional[str] = None
    topic_id: Optional[UUID] = None
    hours_studied: Optional[float] = None
    what_learned: Optional[str] = None
    difficulty: Optional[str] = None
    log_date: Optional[date] = None

class LearningLog(LearningLogBase):
    id: UUID
    created_at: datetime
    log_date: date

    class Config:
        from_attributes = True
