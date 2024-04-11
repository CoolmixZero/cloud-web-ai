from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

def generate_id():
    return str(uuid4())

def generate_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    return str(dt_string)

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    user_id: str = Field(default_factory=generate_id)
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str