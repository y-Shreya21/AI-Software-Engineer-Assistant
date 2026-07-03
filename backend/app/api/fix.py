from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agents import CoordinatorAgent

router = APIRouter()


class FixRequest(BaseModel):

    code: str


@router.post("/generate")
async def generate_fix(
    payload: FixRequest
):

    coordinator = CoordinatorAgent()
    response = coordinator.route_request("suggest fixes", code=payload.code)

    return {
        "fix": response["answer"]
    }