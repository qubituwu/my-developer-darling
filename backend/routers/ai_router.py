from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from enum import Enum
import requests
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
        prompt = assistant_agent.prompt
        graph = assistant_agent.graph
        config = {"configurable": {"thread_id": "1"}}

        events = graph.stream(
            {
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": request.code_snippet},
                ]
            },
            config,
            stream_mode="values",
        )

        feedback = ""
        for event in events:
            if "messages" in event:
                feedback = event["messages"][-1].content

        return {"persona": request.persona, "feedback": feedback}

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

