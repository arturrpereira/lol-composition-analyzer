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

