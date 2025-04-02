from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import decode_token
from app import models
from app.database import get_db

oauth_bearer = OAuth2PasswordBearer("/signin")

async def get_user(token: str = Depends(oauth_bearer), db: AsyncSession = Depends(get_db)):
    user_id = decode_token(token)
    if user_id is None:
        raise HTTPException(401)
    user = await db.get(models.User, user_id)
    if user is None:
        raise HTTPException(401)
    return user

async def get_post(post_id: int, user: models.User = Depends(get_user), db: AsyncSession = Depends(get_db)):
    post = await db.execute(select(models.Post).filter(models.Post.id == post_id, models.Post.user_id == user.id))
    post = post.scalars().first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

CurrentUser = Annotated[models.User, Depends(get_user)]
