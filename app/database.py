from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "mysql+aiomysql://myuser:mypassword@localhost:3306/fastapi"

engine = create_async_engine(url=DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
