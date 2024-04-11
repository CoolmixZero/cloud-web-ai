from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_test_user, get_user_from_db
from routes import auth

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

# init_test_user()
# print(get_user_from_db("coolmix"))