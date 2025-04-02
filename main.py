from fastapi import FastAPI
from app.routes import router
from app.database import engine
from app.models import Base

async def lifespan(_):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/")
async def index():
    return "Hello"