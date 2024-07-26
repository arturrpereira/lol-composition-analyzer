from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from database.db import get_connection
from database.models import User
from schemas.user_schema import CreateUser, CreateUserResponse, LoginRequest
from utils.security import password_hash, verify_password_hash, generate_access_token


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


@router.post("/user/auth")
def add_user_auth(data: LoginRequest, db: Session = Depends(get_connection)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    verify_password = verify_password_hash(data.password, user.hashed_password)
    if not verify_password:
        raise HTTPException(status_code=401, detail="Incorret password")
    
    expires = timedelta(days=1)
    access_token = generate_access_token({"sub": data.username},expires_delta=expires)

    response = JSONResponse(content={"access_token": access_token.access_token, "token_type": access_token.token_type})
    response.set_cookie(
        key="access_token",
        value=access_token.access_token,
        httponly=True,
        secure=False,
        expires=expires
    )
    return response

