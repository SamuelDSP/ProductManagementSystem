from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    role: Mapped[str] = mapped_column(String, default="user", nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)