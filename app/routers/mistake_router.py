from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import mistake_model
from ..schemas import mistake_schema

router = APIRouter()

@router.post("/", response_model=mistake_schema.Mistake)
def create_mistake(mistake: mistake_schema.MistakeCreate, db: Session = Depends(get_db)):
    db_mistake = mistake_model.MistakeModel(**mistake.dict())
    db.add(db_mistake)
    db.commit()
    db.refresh(db_mistake)
    return db_mistake

@router.get("/", response_model=List[mistake_schema.Mistake])
def read_mistakes(db: Session = Depends(get_db)):
    return db.query(mistake_model.MistakeModel).order_by(mistake_model.MistakeModel.date.desc()).all()

@router.put("/{mistake_id}", response_model=mistake_schema.Mistake)
def update_mistake(mistake_id: UUID, mistake_update: mistake_schema.MistakeUpdate, db: Session = Depends(get_db)):
    db_mistake = db.query(mistake_model.MistakeModel).filter(mistake_model.MistakeModel.id == mistake_id).first()
    if not db_mistake:
        raise HTTPException(status_code=404, detail="Mistake not found")
    
    update_data = mistake_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_mistake, key, value)
    
    db.commit()
    db.refresh(db_mistake)
    return db_mistake

@router.delete("/{mistake_id}")
def delete_mistake(mistake_id: UUID, db: Session = Depends(get_db)):
    db_mistake = db.query(mistake_model.MistakeModel).filter(mistake_model.MistakeModel.id == mistake_id).first()
    if not db_mistake:
        raise HTTPException(status_code=404, detail="Mistake not found")
    
    db.delete(db_mistake)
    db.commit()
    return {"message": "Mistake deleted successfully"}
