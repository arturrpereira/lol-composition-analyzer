import jwt
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from schemas.token_schema import Token


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def password_hash(password):
    return context.hash(password)


def verify_password_hash(password, hashed_password):
    return context.verify(password, hashed_password)


def generate_access_token(data, expires_delta):
    encoded_data = data.copy()

    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=15)

    encoded_data.update({"exp": expires})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, ALGORITHM)
