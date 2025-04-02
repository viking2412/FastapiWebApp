from fastapi import APIRouter, HTTPException

from .dependencies import CurrentDB, CurrentUser, CurrentPost
from .schemas import UserCreate, UserLogin, PostCreate
from .services import create_post, create_user, authenticate_user, find_post
from .auth import create_token

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate, db: CurrentDB):
    user =  await create_user(db, user.email, user.password)
    token = create_token(user.id)
    return {"token": token}

@router.post("/login")
async def login(user: UserLogin, db: CurrentDB):
    token = await authenticate_user(db, user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": token}

@router.post("/posts")
async def add_post(post: PostCreate, user: CurrentUser, db: CurrentDB):
    new_post_id = await create_post(db, user, post.text)
    return {"postID": new_post_id}

@router.get("/posts")
async def get_posts(user: CurrentUser, db: CurrentDB):
    posts = await find_post(db, user)
    return posts

@router.delete("/posts/{post_id}")
async def delete_post(post: CurrentPost, db: CurrentDB):
    await db.delete(post)
    await db.commit()
    return {"detail": "Post deleted"}
