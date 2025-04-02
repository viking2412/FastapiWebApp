from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, Post
from .auth import hash_password, verify_password, create_token

async def create_user(db: AsyncSession, email: str, password: str):
    hashed_pw = hash_password(password)
    user = User(email=email, password_hash=hashed_pw)
    db.add(user)
    await db.commit()
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user and verify_password(password, user.password_hash):
        return create_token(user.id)
    return None
