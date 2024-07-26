from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.db import get_connection
from database.models import User
from schemas.user_schema import CreateUser, CreateUserResponse
from utils.security import password_hash

router = APIRouter()


@router.post("/user")
def add_user(user: CreateUser, db: Session = Depends(get_connection)):
    
    hashed_password = password_hash(user.password)
    user.password = hashed_password

    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return CreateUserResponse(message="Create user successfully", user=user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already registered!")
