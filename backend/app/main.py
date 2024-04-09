from fastapi import FastAPI, Body, Depends

from model import PostSchema, UserSchema, UserLoginSchema
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
import logging

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users = []

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Adjust logging level as needed

# helpers

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# route handlers

@app.get("/", tags=["root"])
async def read_root() -> dict:
    logger.info("Root endpoint accessed.")  # Log root access
    return {"message": "Welcome to your blog!"}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    logger.info("Get all posts requested.")  # Log request for all posts
    return {"data": posts}


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        logger.error(f"Invalid post ID requested: {id}")  # Log error for invalid ID
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            logger.info(f"Post with ID {id} retrieved successfully.")  # Log successful retrieval
            return {"data": post}


@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    logger.info(f"Post added successfully. New ID: {post.id}")  # Log successful post addition
    return {"data": "post added."}


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)  # replace with db call, making sure to hash the password first
    logger.info(f"New user created with email: {user.email}")  # Log user creation
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        logger.info(f"User login successful for email: {user.email}")  # Log successful login
        return signJWT(user.email)
    logger.warning(f"Failed login attempt for email: {user.email}")  # Log failed login attempt
    return {
        "error": "Wrong login details!"
    }