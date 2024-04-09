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

logging.getLogger('passlib').setLevel(logging.ERROR)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class User(BaseModel):
    id: str
    username: str
    role: str | None
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


fake_users_db = {
    "johndoe": {
        "id": str(uuid.uuid4),
        "username": "johndoe",
        "role": "user",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "id": str(uuid.uuid4),
        "username": "alice",
        "role": "user",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}


def get_user(db, username: str):
    if username in db:
        user_dict = db.get(username)
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str, db):
    user = get_user(db, username)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, id: str, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


@router.post("/", status_code=status.HTTP_201_CREATED, description="Sign-up endpoint")
async def create_user(create_user_request: CreateUserRequest):
    if create_user_request.username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already registered")
    
    hashed_password = bcrypt_context.hash(create_user_request.password)
    fake_users_db[create_user_request.username] = {
        "id": str(uuid.uuid4),
        "username": create_user_request.username,
        "full_name": f"{create_user_request.first_name} {create_user_request.last_name}",
        "email": create_user_request.email,
        "hashed_password": hashed_password,
        "disabled": False,
    }
    return {"message": "User created successfully"}


@router.post("/token", response_model=Token, description="Login endpoint")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, fake_users_db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(user.username, user.id, user.role, access_token_expires)

    return Token(access_token=access_token, token_type="bearer")