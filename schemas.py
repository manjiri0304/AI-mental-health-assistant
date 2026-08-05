from pydantic import BaseModel

class JournalCreate(BaseModel):
    journal: str
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
class UserLogin(BaseModel):
    email: str
    password: str