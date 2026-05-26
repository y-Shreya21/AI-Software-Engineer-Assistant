from fastapi import APIRouter
from pydantic import BaseModel

import ollama

router = APIRouter()


class TestRequest(BaseModel):

    code: str


@router.post("/generate")
async def generate_tests(
    payload: TestRequest
):

    prompt = f"""
You are an expert Python test engineer.

Generate high-quality pytest unit tests
for the following code.

Code:
{payload.code}

Requirements:
- Use pytest
- Include edge cases
- Include mocks if needed
- Write production-quality tests
"""

    response = ollama.chat(
        model="llama3",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "tests":
        response["message"]["content"]
    }