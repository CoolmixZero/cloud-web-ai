from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4
from datetime import datetime


def generate_id():
    return str(uuid4())

def generate_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    return str(dt_string)

class UserHistoryData(BaseModel):
    user_id: str
    username: str
    image_name: str
    model_result: str
    created_at: str = Field(default_factory=generate_date)

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "username": "kekic",
                "email": "whoisdis@x.com",
                "password": "weakpassword"
            }
        }
        

class LoginUserRequest(BaseModel):
    username: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "username": "kekic",
                "password": "weakpassword"
            }
        }


class User(BaseModel):
    user_id: str = Field(default_factory=generate_id)
    username: str
    email: EmailStr | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str