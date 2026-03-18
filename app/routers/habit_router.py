from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import date
from ..database import get_db
from ..models import habit_model
from ..schemas import habit_schema

router = APIRouter()

@router.post("/", response_model=habit_schema.Habit)
def create_habit(habit: habit_schema.HabitCreate, db: Session = Depends(get_db)):
    db_habit = habit_model.HabitModel(**habit.dict())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.get("/", response_model=List[habit_schema.Habit])
def read_habits(db: Session = Depends(get_db)):
    return db.query(habit_model.HabitModel).all()

@router.post("/log")
def log_habit(habit_id: UUID, log_date: date, completed: bool, db: Session = Depends(get_db)):
    db_log = habit_model.HabitLogModel(habit_id=habit_id, log_date=log_date, completed=completed)
    db.add(db_log)
    
    # Simple streak logic: if completed, check previous days
    # (Detailed logic can be added later)
    if completed:
        db_habit = db.query(habit_model.HabitModel).filter(habit_model.HabitModel.id == habit_id).first()
        if db_habit:
            db_habit.streak += 1
            
    db.commit()
    return {"status": "logged"}

@router.put("/{habit_id}", response_model=habit_schema.Habit)
def update_habit(habit_id: UUID, habit_update: habit_schema.HabitUpdate, db: Session = Depends(get_db)):
    db_habit = db.query(habit_model.HabitModel).filter(habit_model.HabitModel.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    update_data = habit_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_habit, key, value)
    
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.delete("/{habit_id}")
def delete_habit(habit_id: UUID, db: Session = Depends(get_db)):
    db_habit = db.query(habit_model.HabitModel).filter(habit_model.HabitModel.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    db.delete(db_habit)
    db.commit()
    return {"message": "Habit deleted successfully"}
