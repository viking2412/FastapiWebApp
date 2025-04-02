import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Post, User
from .auth import hash_password, verify_password, create_token

cache = {}

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

async def create_post(db: AsyncSession, user: User, post_contains: str):
    new_post = Post(text=post_contains, user_id=user.id)
    db.add(new_post)
    await db.commit()
    return new_post.id

async def find_post(db: AsyncSession, user: User):
    posts = await db.execute(select(Post).filter(Post.user_id == user.id))
    if user.id not in cache:
        cache[user.id] = {}
    cache[user.id] = posts
    asyncio.create_task(remove_from_cache(user.id))
    return cache[user.id].scalars().all()

"""def cached_posts(get_posts):
    def wrapper(user: User):
        if datetime.timestamp - cache[user.id[1]] <= 300 :
            return cache[user.id[0]]
        else:
            time = datetime.timestamp
            cache[user.id] = (get_posts(), time)"""

async def remove_from_cache(user_id: int, delay: int = 300):
    """Removes a cached entry after 'delay' seconds (default: 5 minutes)."""
    await asyncio.sleep(delay)
    if user_id in cache:
        del cache[user_id]
        """if not cache[user_id]:
            del cache.keys[user_id]"""
    #print("CACHE DELETED")
    