from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_engineer",
    )
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-jwt-signing-key-for-local-development")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

settings = Settings()