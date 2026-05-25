from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.base import Base
# Import the actual APIRouter instance and rename it to repo_router
from app.api.repositories import router as repo_router
from app.services.qdrant_service import create_collection
from app.api.search import router as search_router
from app.api.chat import router as chat_router
from app.api import architecture


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    create_collection()
    yield


app = FastAPI(
    title="AI Software Engineer Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)
app.include_router(
    architecture.router,
    prefix="/architecture",
    tags=["Architecture"]
)