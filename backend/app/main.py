from fastapi import FastAPI

from app.db.database import engine
from app.db.base import Base
# Import the actual APIRouter instance and rename it to repo_router
from app.api.repositories import router as repo_router
from app.services.qdrant_service import create_collection
from app.api.search import router as search_router

app = FastAPI(
    title="AI Software Engineer Assistant",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    create_collection()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

# Register the router
app.include_router(
    repo_router,
    prefix="/repos",
    tags=["Repositories"]
)
app.include_router(
    search_router,
    prefix="/search",
    tags=["Search"]
)