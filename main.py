from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from security import verify_password, create_access_token
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

from schemas import JournalCreate, UserCreate, UserLogin
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
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)

    return {
        "message": "User registered successfully!",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db, user.email)

    if not db_user:
        return {
            "message": "User not found!"
        }

    if not verify_password(user.password, db_user.password):
        return {
            "message": "Incorrect password!"
        }

    token = create_access_token(
    {
        "user_id": db_user.id,
        "email": db_user.email
    }
)

    return {
    "message": "Login Successful!",
    "access_token": token,
    "token_type": "bearer",
    "user_id": db_user.id,
    "name": db_user.name,
    "email": db_user.email
}