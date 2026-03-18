from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from uuid import UUID

class MilestoneBase(BaseModel):
    title: str
    description: Optional[str] = None
    target_date: Optional[str] = None
    status: Optional[str] = "planned"
    tags: Optional[List[str]] = []
    icon_name: Optional[str] = "Target"

class MilestoneCreate(MilestoneBase):
    pass

class MilestoneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    icon_name: Optional[str] = None

class Milestone(MilestoneBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
