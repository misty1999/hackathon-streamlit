from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.security import get_current_user
from database.database import get_db
from database.models import Note
from schemas.note import NoteCreate, NoteUpdate, Note as NoteSchema
from sqlalchemy import or_

router = APIRouter()

@router.post("/notes/", response_model=NoteSchema)
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_note = Note(
        title=note.title,
        content=note.content,
        parent_id=note.parent_id,
        user_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/notes/", response_model=List[NoteSchema])
def get_notes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Note).filter(Note.user_id == current_user.id, Note.parent_id == None).all()

@router.get("/notes/{note_id}", response_model=NoteSchema)
def get_note(note_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/notes/{note_id}", response_model=NoteSchema)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    for field, value in note.dict(exclude_unset=True).items():
        setattr(db_note, field, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}

@router.get("/notes/search/", response_model=List[NoteSchema])
def search_notes(query: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Note).filter(
        Note.user_id == current_user.id,
        or_(
            Note.title.ilike(f"%{query}%"),
            Note.content.ilike(f"%{query}%")
        )
    ).all()
