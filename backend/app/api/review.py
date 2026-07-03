from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agents import CoordinatorAgent

router = APIRouter()


class ReviewRequest(BaseModel):

    code: str


@router.post("/analyze")
async def analyze_code(
    payload: ReviewRequest
):

    coordinator = CoordinatorAgent()
    response = coordinator.route_request("explain code", code=payload.code)

    return {
        "review": response["answer"]
    }