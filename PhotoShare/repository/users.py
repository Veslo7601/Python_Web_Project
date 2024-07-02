from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from PhotoShare.database.database import get_database
from PhotoShare.database.models import User, Role
from PhotoShare.schemas import UserSchema, UserUpdateSchema


async def get_user_by_username(username: str, db: AsyncSession = Depends(get_database)):
    """
    Get user by username from database

    :param username: str
    :param db: AsyncSession
    :return: User
    """

    stmt = select(User).filter_by(username=username)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_database)):
    """
    Get user by email from database

    :param email: str
    :param db: AsyncSession
    :return: User
    """

    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_database)):
    """
    Create new user in database

    :param body: UserSchema
    :param db: AsyncSession
    :return: User
    """

    avatar: Optional[str] = None
    new_user = User(**body.model_dump(), avatar=avatar)
    print(new_user)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    if new_user.id == 1:
        new_user.role = Role.admin
        await db.commit()
        await db.refresh(new_user)

    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    Update user token in database

    :param user: User
    :param token: str
    :param db: AsyncSession
    :return: User
    """

    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Confirmed email in database

    :param email: str
    :param db: AsyncSession
    :return: None
    """

    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    Update avatar url in database

    :param email: str
    :param url: str
    :param db: AsyncSession
    :return: User
    """

    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(body: UserUpdateSchema, db: AsyncSession, user: User):
    """
    Update user in database

    :param body: UserUpdateSchema
    :param db: AsyncSession
    :param user: User
    :return: User
    """

    stmt = select(User).filter_by(id=user.id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    for key, value in body.dict().items():
        if value is not None:
            setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


async def block_user(user: User, db: AsyncSession = Depends(get_database)):
    """
    Block user in database

    :param user: User
    :param db: AsyncSession
    :return: None
    """
    user.blocked = True
    await db.commit()
