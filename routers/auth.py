from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from database import get_db
from schemas import UserCreate, UserLogin
from security import verify_password, create_access_token
router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)

    return {
        "message": "User registered successfully!",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }

@router.post("/login")
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
