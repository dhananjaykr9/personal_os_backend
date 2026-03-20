from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import learning_model
from ..schemas import learning_schema

router = APIRouter()

@router.post("/", response_model=learning_schema.RoadmapSkill)
def create_skill(skill: learning_schema.RoadmapSkillCreate, db: Session = Depends(get_db)):
    # Check for existing skill
    existing = db.query(learning_model.RoadmapSkillModel).filter(learning_model.RoadmapSkillModel.skill_name == skill.skill_name).first()
    if existing:
        return existing
        
    db_skill = learning_model.RoadmapSkillModel(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.get("/", response_model=List[learning_schema.RoadmapSkill])
def read_roadmap(db: Session = Depends(get_db)):
    return db.query(learning_model.RoadmapSkillModel).all()

@router.patch("/{skill_id}", response_model=learning_schema.RoadmapSkill)
def update_skill(skill_id: UUID, skill: learning_schema.RoadmapSkillUpdate, db: Session = Depends(get_db)):
    db_skill = db.query(learning_model.RoadmapSkillModel).filter(learning_model.RoadmapSkillModel.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    update_data = skill.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_skill, key, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.delete("/{skill_id}")
def delete_skill(skill_id: UUID, db: Session = Depends(get_db)):
    db_skill = db.query(learning_model.RoadmapSkillModel).filter(learning_model.RoadmapSkillModel.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(db_skill)
    db.commit()
    return {"message": "Skill deleted successfully"}
