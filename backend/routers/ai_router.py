from fastapi import APIRouter
from pydantic import BaseModel
from enum import Enum
from backend.ai.persona_engine import generate_feedback

router = APIRouter()

class Persona(str, Enum):
    shy = "shy"
    assertive = "assertive"
    silly = "silly"

class CodeFeedbackRequest(BaseModel):
    code_snippet: str
    persona: Persona

@router.post("/feedback")
async def get_code_feedback(request: CodeFeedbackRequest):
    feedback = generate_feedback(request.code_snippet, request.persona.value)
    return {"persona": request.persona, "feedback": feedback}
