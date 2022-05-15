from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import AsyncSession, Column, String
from fastapi import Depends
from typing import AsyncGenerator


DATABASE_URL = "sqlite+aiosqlite:///./test.db"
Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    role = Column(String)
    # pass


engine = create_async_engine(DATABASE_URL, echo=True)
# engine = create_async_engine(DATABASE_URL, connect_args={
#                              "check_same_thread": False})
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, autocommit=False, expire_on_commit=False, autoflush=False)


# def run_upgrade(connection, cfg):
#     cfg.attributes["connection"] = connection
#     command.upgrade(cfg, "head")


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
