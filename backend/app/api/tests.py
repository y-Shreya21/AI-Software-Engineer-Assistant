from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agents import CoordinatorAgent

router = APIRouter()


class TestRequest(BaseModel):

    code: str


@router.post("/generate")
async def generate_tests(
    payload: TestRequest
):

    coordinator = CoordinatorAgent()
    response = coordinator.route_request("generate tests", code=payload.code)

    return {
        "tests": response["answer"]
    }