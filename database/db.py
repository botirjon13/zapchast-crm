import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, select

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"  # O'zgartiring!

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    role = Column(String, default="customer")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_user_role(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalars().first()
        if user:
            return user.role
        return None

async def add_user(telegram_id: int, username: str, role: str = "customer"):
    async with async_session() as session:
        user = User(telegram_id=telegram_id, username=username, role=role)
        session.add(user)
        await session.commit()
