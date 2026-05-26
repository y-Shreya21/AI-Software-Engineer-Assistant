from fastapi import APIRouter
from pydantic import BaseModel

import ollama

router = APIRouter()


class ReviewRequest(BaseModel):

    code: str


@router.post("/analyze")
async def analyze_code(
    payload: ReviewRequest
):

    prompt = f"""
You are an expert senior software engineer.

Analyze the following code for:

- bugs
- bad practices
- performance issues
- async issues
- security problems
- architecture concerns

Then provide:
1. Problems found
2. Explanation
3. Suggested fixes

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
        "review":
        response["message"]["content"]
    }