from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..database import Base

class MilestoneModel(Base):
    __tablename__ = "milestones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    target_date = Column(String, nullable=True) # e.g. "Q1 2026"
    status = Column(String, default="planned") # completed, in-progress, planned
    tags = Column(JSON, default=[])
    icon_name = Column(String, default="Target")
    created_at = Column(DateTime, default=datetime.utcnow)
