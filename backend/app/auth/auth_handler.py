import time
from typing import Dict

import jwt
from decouple import config



# Placeholder values for development
JWT_SECRET = config("secret", default='eyJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzIjoiMjAyNC0wNC0wOVQxMTowNDo0Ni4wODVaIiwidXNlcl9pZCI6Iklzc3VlciJ9.wcz-jUkpxNM98HrZ4jHmrBTwyfv71RyqowwsdrehGow')
JWT_ALGORITHM = config("algorithm", default="HS256")


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 60000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
