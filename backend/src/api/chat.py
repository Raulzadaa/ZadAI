from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from .deps import require_user_api, require_user_page
from .templating import render
from .zadai_client import ZadAIUnavailable, ask_zadai

router = APIRouter()


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=8000)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1, max_length=40)


class ChatResponse(BaseModel):
    reply: str


@router.get("/chat", include_in_schema=False, dependencies=[Depends(require_user_page)])
async def chat_page(request: Request):
    return render(request, "chat.html", active="chat")


@router.post("/api/chat", response_model=ChatResponse, dependencies=[Depends(require_user_api)])
async def chat(body: ChatRequest):
    if body.messages[-1].role != "user":
        raise HTTPException(status_code=422, detail="A última mensagem precisa ser do usuário.")
    try:
        reply = await ask_zadai([m.model_dump() for m in body.messages])
    except ZadAIUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return ChatResponse(reply=reply)
