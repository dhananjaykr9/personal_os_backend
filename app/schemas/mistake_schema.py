import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MistakeBase(BaseModel):
    topic: str
    mistake_content: str
    correct_understanding: Optional[str] = None
    importance: Optional[str] = "medium"
    date: Optional[datetime.date] = None

class MistakeCreate(MistakeBase):
    pass

class MistakeUpdate(BaseModel):
    topic: Optional[str] = None
    mistake_content: Optional[str] = None
    correct_understanding: Optional[str] = None
    importance: Optional[str] = None
    date: Optional[datetime.date] = None

class Mistake(MistakeBase):
    id: UUID
    date: datetime.date
    created_at: datetime.datetime

    class Config:
        from_attributes = True
