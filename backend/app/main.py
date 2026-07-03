from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.base import Base
# Import the actual APIRouter instance and rename it to repo_router
from app.api.repositories import router as repo_router
from app.services.qdrant_service import create_collection
from app.api.search import router as search_router
from app.api.chat import router as chat_router
from app.api import architecture
from app.api import tests
from app.api import review
from app.api import fix
from app.api.auth import router as auth_router
from app.core.rate_limit import rate_limiter


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
    dependencies=[Depends(rate_limiter)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://10.162.64.181:3000",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    from app.core.metrics import increment_request_count
    increment_request_count(request.method, request.url.path)
    
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
    return response

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

@app.get("/metrics")
async def metrics_endpoint():
    from fastapi import Response
    from app.core.metrics import generate_prometheus_report
    return Response(content=generate_prometheus_report(), media_type="text/plain")

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
app.include_router(
    tests.router,
    prefix="/tests",
    tags=["Tests"]
)
app.include_router(
    review.router,
    prefix="/review",
    tags=["Review"]
)
app.include_router(
    fix.router,
    prefix="/fix",
    tags=["Fix"]
)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)