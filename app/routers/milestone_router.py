from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import milestone_model
from ..schemas import milestone_schema

router = APIRouter()

@router.get("/", response_model=List[milestone_schema.Milestone])
def read_milestones(db: Session = Depends(get_db)):
    return db.query(milestone_model.MilestoneModel).order_by(milestone_model.MilestoneModel.created_at).all()

@router.post("/", response_model=milestone_schema.Milestone)
def create_milestone(milestone: milestone_schema.MilestoneCreate, db: Session = Depends(get_db)):
    db_milestone = milestone_model.MilestoneModel(**milestone.dict())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.patch("/{milestone_id}", response_model=milestone_schema.Milestone)
def update_milestone(milestone_id: UUID, milestone: milestone_schema.MilestoneUpdate, db: Session = Depends(get_db)):
    db_milestone = db.query(milestone_model.MilestoneModel).filter(milestone_model.MilestoneModel.id == milestone_id).first()
    if not db_milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    
    update_data = milestone.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_milestone, key, value)
    
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.delete("/{milestone_id}")
def delete_milestone(milestone_id: UUID, db: Session = Depends(get_db)):
    db_milestone = db.query(milestone_model.MilestoneModel).filter(milestone_model.MilestoneModel.id == milestone_id).first()
    if not db_milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    db.delete(db_milestone)
    db.commit()
    return {"message": "Milestone deleted"}
