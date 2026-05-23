from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import search_similar_code

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/")
async def semantic_search(payload: SearchRequest):

    query_embedding = generate_embedding(
        payload.query
    )

    results = search_similar_code(
        query_embedding
    )

    formatted_results = []

    for result in results:

        formatted_results.append({
            "score": result.score,
            "file_path": result.payload.get("file_path"),
            "content": result.payload.get("content")
        })

    return {
        "query": payload.query,
        "results": formatted_results
    }