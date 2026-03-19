from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Dict, Any
from uuid import UUID

class LearningTopicBase(BaseModel):
    topic: str
    category: Optional[str] = None
    completion_percentage: Optional[int] = 0
    hours_spent: Optional[float] = 0.0
    status: Optional[str] = "not_started"
    syllabus: Optional[Dict[str, Any]] = None

class LearningTopicCreate(LearningTopicBase):
    pass

class LearningTopicUpdate(BaseModel):
    topic: Optional[str] = None
    category: Optional[str] = None
    completion_percentage: Optional[int] = None
    hours_spent: Optional[float] = None
    status: Optional[str] = None
    syllabus: Optional[Dict[str, Any]] = None

class LearningTopic(LearningTopicBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class RoadmapSkillBase(BaseModel):
    skill_name: str
    category: Optional[str] = None
    difficulty: Optional[str] = None
    importance: Optional[str] = "medium"
    status: Optional[str] = "not_started"
    completion_date: Optional[date] = None

class RoadmapSkillCreate(RoadmapSkillBase):
    pass

class RoadmapSkillUpdate(BaseModel):
    skill_name: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    importance: Optional[str] = None
    status: Optional[str] = None
    completion_date: Optional[date] = None

class RoadmapSkill(RoadmapSkillBase):
    id: UUID

    class Config:
        from_attributes = True
