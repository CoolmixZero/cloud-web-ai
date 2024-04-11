from datetime import timedelta, datetime, timezone
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import uuid

from database import create_new_user, get_user_from_db
from models import Token, CreateUserRequest, User, UserInDB

logging.getLogger('passlib').setLevel(logging.ERROR)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')



def authenticate_user(username: str, password: str):
    user = get_user_from_db(username)
    if user is None:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = {'sub': username, 'user_id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('user_id')
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'user_id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED, description="Sign-up endpoint")
async def create_user(create_user_request: CreateUserRequest) -> Token:
    user_in_db = get_user_from_db(create_user_request.username) is not None
    if user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already registered")
    
    hashed_password = bcrypt_context.hash(create_user_request.password)
    
    user_in_db_obj = {
        "username": create_user_request.username,
        "email": create_user_request.email,
        "hashed_password": hashed_password,
        "disabled": False,
    }
    new_user = UserInDB(**user_in_db_obj)
    
    status_code = create_new_user(new_user.dict())
    
    if status_code not in [200, 201]:
        raise("Error when creating user in DynamoDB")
    
    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(new_user.username, new_user.user_id, access_token_expires)
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login", response_model=Token, description="Login endpoint")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(user.username, user.user_id, access_token_expires)

    return Token(access_token=access_token, token_type="bearer")