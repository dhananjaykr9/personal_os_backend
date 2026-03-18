from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import note_model
from ..schemas import note_schema

router = APIRouter()

@router.post("/", response_model=note_schema.Note)
def create_note(note: note_schema.NoteCreate, db: Session = Depends(get_db)):
    db_note = note_model.NoteModel(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=List[note_schema.Note])
def read_notes(search: str = None, db: Session = Depends(get_db)):
    query = db.query(note_model.NoteModel)
    if search:
        query = query.filter(note_model.NoteModel.title.ilike(f"%{search}%") | note_model.NoteModel.content.ilike(f"%{search}%"))
    return query.all()

@router.get("/{note_id}", response_model=note_schema.Note)
def read_note(note_id: UUID, db: Session = Depends(get_db)):
    note = db.query(note_model.NoteModel).filter(note_model.NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=note_schema.Note)
def update_note(note_id: UUID, note: note_schema.NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(note_model.NoteModel).filter(note_model.NoteModel.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    update_data = note.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_note, key, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
def delete_note(note_id: UUID, db: Session = Depends(get_db)):
    note = db.query(note_model.NoteModel).filter(note_model.NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"status": "deleted"}
