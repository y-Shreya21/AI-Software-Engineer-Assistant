from fastapi import APIRouter
from pydantic import BaseModel

import ollama

router = APIRouter()


class FixRequest(BaseModel):

    code: str


@router.post("/generate")
async def generate_fix(
    payload: FixRequest
):

    prompt = f"""
You are an expert senior software engineer.

Analyze the following code.

Fix:
- bugs
- bad practices
- performance issues
- async issues
- architecture problems

Return:
1. Improved code
2. Explanation of fixes

Code:
{payload.code}
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
        "fix":
        response["message"]["content"]
    }