from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.models import User
from PhotoShare.schemas import UserModel


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    return db.query(User).filter(User.email == email).first()


async def get_user_by_username(username: str, db: AsyncSession) -> User:
    return db.query(User).filter(User.username == username).first()


async def create_user(body: UserModel, db: AsyncSession) -> User:
    new_user = User(**body.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()
