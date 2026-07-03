from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.models.user import User, Workspace
from app.models.chat import ChatMessage
