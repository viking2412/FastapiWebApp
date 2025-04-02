from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Post, User
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

async def create_post(db: AsyncSession, user = User, post_contains = str):
    new_post = Post(text=post_contains, user_id=user.id)
    db.add(new_post)
    await db.commit()
    return new_post.id

async def find_post(db: AsyncSession, user = User):
    posts = await db.execute(select(Post).filter(Post.user_id == user.id))
    return posts.scalars().all()

