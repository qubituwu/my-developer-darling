from pydantic import BaseModel
from enum import Enum

# Pydantic schema for reading and writing data
class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(BaseModel):
    name: str
    description: str

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries

class Persona(str, Enum):
    shy = "shy"
    assertive = "assertive"
    silly = "silly"

class CodeFeedbackRequest(BaseModel):
    code_snippet: str
    persona: Persona
