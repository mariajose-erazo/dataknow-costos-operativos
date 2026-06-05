from pathlib import Path
import sys
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

from agent import answer_with_local_context, check_agent_ready


app = FastAPI(
    title="Agente IA - Costos Operativos",
    description="API para consultar resultados del análisis, modelado y forecasting.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=PROJECT_ROOT / "app" / "static"),
    name="static",
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    answer: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "agent": check_agent_ready(),
    }


@app.get("/", response_class=HTMLResponse)
def home():
    index_path = PROJECT_ROOT / "app" / "templates" / "index.html"
    return index_path.read_text(encoding="utf-8")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="La pregunta no puede estar vacía.",
        )

    try:
        history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.history
        ]

        answer = answer_with_local_context(
            question=request.question,
            history=history,
        )

        return ChatResponse(answer=answer)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))