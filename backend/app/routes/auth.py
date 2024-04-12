from os import getenv
from datetime import timedelta, datetime, timezone
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from ..database import create_new_user, get_user_from_db
from ..models import LoginUserRequest, Token, CreateUserRequest, UserInDB

logging.getLogger('passlib').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

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
    return jwt.encode(encode, getenv("JWT_SECRET_KEY"), algorithm=getenv("ALGORITHM"))

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, getenv("JWT_SECRET_KEY"), algorithms=getenv("ALGORITHM"))
        username: str = payload.get('sub')
        user_id: str = payload.get('user_id')
        if username is None or id is None:
            logger.error('Invalid token. Username or user_id is None.')
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'user_id': user_id}
    except JWTError:
        logger.error('JWT Error. Failed to decode token.')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

@router.post("/register", status_code=status.HTTP_201_CREATED, description="Sign-up endpoint")
async def create_user(create_user_request: CreateUserRequest) -> dict:
    user_in_db = get_user_from_db(create_user_request.username) is not None
    if user_in_db:
        logger.warning(f"User '{create_user_request.username}' already registered.")
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
        logger.error("Error when creating user in DynamoDB")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error when creating user in DynamoDB")
    
    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(new_user.username, new_user.user_id, access_token_expires)
    
    response = {
        "status": 201,
        "result": Token(access_token=access_token, token_type="bearer").dict()
    }
    
    logger.info(f"User '{create_user_request.username}' registered successfully.")
    return response

@router.post("/login", description="Login endpoint")
async def login_for_access_token(
    form_data: LoginUserRequest,
) -> dict:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for user '{form_data.username}'. Incorrect username or password.")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(user.username, user.user_id, access_token_expires)

    response = {
        "status": 200,
        "result": Token(access_token=access_token, token_type="bearer").dict()
    }
    
    logger.info(f"User '{user.username}' logged in successfully.")
    return response