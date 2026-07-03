from fastapi import APIRouter
from pydantic import BaseModel

from fastapi.responses import StreamingResponse

from app.services.agents import CoordinatorAgent
from app.services.ai_services import stream_repository_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/")
async def chat_with_repo(payload: ChatRequest):

    coordinator = CoordinatorAgent()
    response = coordinator.route_request(payload.question)

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