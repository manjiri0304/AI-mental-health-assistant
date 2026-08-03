from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
import crud

from fastapi import FastAPI
from database import engine
from models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Powered Mental Health Assistant!"
    }


@app.get("/health")
def health():
    return {
        "status": "Backend is Running Successfully!"
    }


@app.get("/about")
def about():
    return {
        "project": "AI Powered Mental Health Assistant",
        "team": [
            "Manjiri Barve",
            "Jyoti Gupta",
            "Aiswarya G",
            "Anchal Chaubey"
        ]
    }

from schemas import JournalCreate
@app.post("/journal")
def save_journal(
    data: JournalCreate,
    db: Session = Depends(get_db)
):
    saved_journal = crud.create_journal(db, data.journal)

    return {
    "message": "Journal saved successfully!",
    "id": saved_journal.id,
    "journal": saved_journal.journal
}
@app.get("/journals")
def read_journals(db: Session = Depends(get_db)):
    journals = crud.get_journals(db)
    return journals
@app.put("/journal/{journal_id}")
def edit_journal(
    journal_id: int,
    data: JournalCreate,
    db: Session = Depends(get_db)
):
    updated = crud.update_journal(db, journal_id, data.journal)

    if updated:
        return {
            "message": "Journal updated successfully!",
            "journal": updated
        }

    return {
        "message": "Journal not found!"
    }