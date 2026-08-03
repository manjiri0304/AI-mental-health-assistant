from sqlalchemy import Column, Integer, String
from database import Base

class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)
    journal = Column(String, nullable=False)