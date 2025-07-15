from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

import asyncio
from typing import Union
from os import getenv

load_dotenv()

sync_engine = create_engine(getenv("URL_SYNC_DB"))
sync_session = sessionmaker(bind=sync_engine)

async_engine = create_async_engine(getenv("URL_ASYNC_DB"))
async_session = async_sessionmaker(bind=async_engine)

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)

    def __repr__(self):
        return f"id: {self.id} | user_id: {self.user_id} | username: {self.username}"


class Admins(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(unique=True)

    def __repr__(self):
        return f"id: {self.id}\nuser_id: {self.user_id}\nusername: {self.username}"


async def create_table_users():
    async with async_engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)
        await connect.run_sync(Base.metadata.create_all)


async def create_user(user_id: str, username: Union[str, None]):
    async with async_session() as session:
        user = Users(user_id=user_id, username=username)
        session.add(user)

        await session.commit()


async def check_user_in_db(user_id: str):
    async with async_session() as session:
        query = select(Users).where(Users.user_id == user_id)
        result = await session.execute(query)

        return bool(result.fetchone())


async def get_user(user_id: str):
    async with async_session() as session:
        query = select(Users).where(Users.user_id == user_id)
        result = await session.execute(query)

        return result.fetchone()


async def count_all_users(count: int):
    async with async_session() as session:
        query = select(Users)
        result = await session.execute(query)

        if count == 1:
            return len(result.fetchall())
        else:
            return result.fetchall()


async def check_admin_in_db(admin_id: str):
    async with async_session() as session:
        query = select(Admins).where(Admins.user_id == admin_id)
        result = await session.execute(query)

        return bool(result.fetchone())


async def create_admin(user_id: str):
    async with async_session() as session:
        admin = Admins(user_id=user_id)
        session.add(admin)

        await session.commit()


def get_admins():
    with sync_session() as session:
        query = select(Admins)
        result = session.execute(query)

        return [int(admin[0].user_id) for admin in result.fetchall()]


async def get_admin(user_id: str):
    async with async_session() as session:
        query = select(Users).where(Users.user_id == user_id) #берем инфу про админа из таблицы юзеров, потому что в ней больше инфы про админа
        admin = await session.execute(query)

        return admin.fetchone()[0]


async def all_admins():
    async with async_session() as session:
        admins = []

        query = select(Admins)
        result = await session.execute(query)

        for admin in [int(admin[0].user_id) for admin in result.fetchall()]:
            admin = await get_user(user_id=str(admin))
            admins.append(admin)

        return admins


async def delete_admin(admin_id: str):
    async with async_session() as session:
        query = delete(Admins).where(Admins.user_id == admin_id)
        await session.execute(query)

        await session.commit()


async def main():
    try:
        await create_table_users()
        await create_admin("5119363066")
    finally:
        await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
