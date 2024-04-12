import logging
import httpx
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
  
import base64
import json

from .auth import get_current_user                    
from ..database import create_new_user, get_user_from_db, get_user_history, insert_to_user_history
from ..models import UserHistoryData

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/upload',
    tags=['upload']
)


@router.post("/image")
async def create_upload_file(file: UploadFile, current_user: dict = Depends(get_current_user)):
    im_bytes = await file.read()    
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    
    data = json.dumps({"image": im_b64})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    # TODO: add url to model endpoint
    url = ""
    # res = httpx.post(url, data=data, headers=headers)
    
    # TODO: get result from response
    result = "yes"
    # data = response.json()
    # print(response.text)
    
    print(current_user)
    
    user_history_obj = {
      "user_id": current_user.get("user_id"),
      "username": current_user.get("username"),
      "image_name": file.filename,
      "model_result": result
    }
    
    user_history = UserHistoryData(**user_history_obj).dict()
    
    # Insert new log to db
    status_code = insert_to_user_history(user_history)
    
    response = response = {
        "status": status_code,
        "result": user_history
    }
    return response
  
@router.get("/history")
async def get_upload_history(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id")
    
    upload_history = get_user_history(user_id)
    
    response = {
        "status": 200,
        "result": upload_history
    }
    
    return response

