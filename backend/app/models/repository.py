from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.git_service import clone_repository
from app.services.file_service import scan_repository

router = APIRouter()

class RepositoryRequest(BaseModel):
    github_url: str

@router.post("/index")
async def index_repository(payload: RepositoryRequest):

    try:

        repo_path = clone_repository(
            payload.github_url
        )

        files = scan_repository(repo_path)

        return {
            "status": "success",
            "total_files": len(files),
            "total_chunks": total_chunks,
            "files": files[:20]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )