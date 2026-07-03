from sqlalchemy.orm import DeclarativeBase
from app.models.user import User, Workspace  # noqa: F401
from app.models.chat import ChatMessage  # noqa: F401


class Base(DeclarativeBase):
    pass
