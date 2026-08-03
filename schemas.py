from pydantic import BaseModel

class JournalCreate(BaseModel):
    journal: str