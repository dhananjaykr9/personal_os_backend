from sqlalchemy import Column, String, Float, Integer, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..database import Base

class LearningTopicModel(Base):
    __tablename__ = "learning_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(String, nullable=False)
    category = Column(String, nullable=True)
    completion_percentage = Column(Integer, default=0)
    hours_spent = Column(Float, default=0.0)
    status = Column(String, default="not_started")
    last_studied_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class RoadmapSkillModel(Base):
    __tablename__ = "roadmap_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    difficulty = Column(String, nullable=True)
    importance = Column(String, default="medium") # low, medium, high
    status = Column(String, default="not_started")
    completion_date = Column(Date, nullable=True)
