from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import CurrentUser, get_post, get_user
from .database import get_db
from .schemas import UserCreate, UserLogin, PostCreate
from .services import create_user, authenticate_user
from .auth import create_token, decode_token
from app.models import Post, User

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user =  await create_user(db, user.email, user.password)
    token = create_token(user.id)
    return {"token": token}


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    token = await authenticate_user(db, user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": token}

@router.post("/posts")
async def add_post(post: PostCreate, user: CurrentUser, db: AsyncSession = Depends(get_db)):
    new_post = Post(text=post.text, user_id=user.id)
    db.add(new_post)
    await db.commit()
    return {"postID": new_post.id}

@router.get("/posts")
async def get_posts(user: CurrentUser, db: AsyncSession = Depends(get_db)):
    posts = await db.execute(select(Post).filter(Post.user_id == user.id))
    return posts.scalars().all()

@router.delete("/posts/{post_id}")
async def delete_post(post: Post = Depends(get_post), db: AsyncSession = Depends(get_db)):
    await db.delete(post)
    await db.commit()
    return {"detail": "Post deleted"}
