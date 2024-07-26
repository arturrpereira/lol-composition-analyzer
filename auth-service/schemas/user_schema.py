from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    message: str
    user: CreateUser


class LoginRequest(BaseModel):
    username: str
    password: str


class LogedUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str


class LogedUserResponse(BaseModel):
    data: LogedUser