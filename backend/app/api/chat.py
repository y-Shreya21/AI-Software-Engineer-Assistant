from fastapi import APIRouter
from pydantic import BaseModel

from fastapi.responses import StreamingResponse

from app.services.ai_services import (
    ask_repository,
    stream_repository_answer,
)

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/")
async def chat_with_repo(payload: ChatRequest):

    response = ask_repository(
        payload.question
    )

    return response
@router.post("/stream")
async def stream_chat(payload: ChatRequest):

    generator = stream_repository_answer(
        payload.question
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )