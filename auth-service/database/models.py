from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.func import func
from database.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, unique=True, index=True, nullable=False)
    last_name = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.utcnow(), nullable=False)
