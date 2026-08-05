from sqlalchemy.orm import Session
from models import Journal, User


def create_journal(db: Session, journal: str):
    new_journal = Journal(journal=journal)
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    return new_journal
def get_journals(db: Session):
    return db.query(Journal).all()
def update_journal(db: Session, journal_id: int, new_text: str):
    journal = db.query(Journal).filter(Journal.id == journal_id).first()

    if journal:
        journal.journal = new_text
        db.commit()
        db.refresh(journal)

    return journal
def delete_journal(db: Session, journal_id: int):
    journal = db.query(Journal).filter(Journal.id == journal_id).first()

    if journal:
        db.delete(journal)
        db.commit()
        return True

    return False
from security import hash_password

def create_user(db: Session, user):
    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()