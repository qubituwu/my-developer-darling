from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from backend.ai.AgentServices import assistant_agent
import httpx

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
    try:
        style = request.persona.value
        prompt = (
            f"You're a software engineer / girlfriend giving feedback on your significant other's code in a {style} tone.\n"
            f"Really try to embody the persona of a girlfriend with a {style} personality.\n"
            f"Please suggest improvements, best practices, or style tips in a flirty manner.\n"
            f"Comments should be short and concise.\n"
            f"Here's the code to review:\n\n"
            "Provide all responses in JSON format: {'feedback': 'string'}\n\n"
        )

        response = assistant_agent.stream_graph_updates(prompt, request.code_snippet)
        return {"persona": request.persona, "feedback": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ChatRequest(BaseModel):
    input: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:11434/api/generate", json={
                "model": "deepseek-coder:latest",
                "prompt": request.input,
                "stream": False
            })
        data = response.json()
        return {"response": data.get("response", "No response from darling model 😢")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DeepSeek error: {str(e)}")
