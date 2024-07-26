from fastapi import APIRouter, Depends, Cookie, HTTPException
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.orm import Session
from typing import Optional
from database.db import get_connection
from database.models import User
from utils.security import decode_access_token
from schemas.user_schema import LogedUser, LogedUserResponse

router = APIRouter()


def verify_access_token(access_token: Optional[str] = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing token in  cookie")

    try:
        decoded_token = decode_access_token(token=access_token)
        return decoded_token
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/user/me")
def read_user_me(
    token: dict = Depends(verify_access_token),
    db: Session = Depends(get_connection),
):
    username = token.get("sub")
    db_user = db.query(User).filter(User.username == username).first()

    data = LogedUser(
        username=db_user.username,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        email=db_user.email,
    )
    return LogedUserResponse(data=data)
