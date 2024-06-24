from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.models import User, Images
from PhotoShare.repository.users import get_user_by_email
from PhotoShare.schemas import ImageSchema


async def add_image(body: ImageSchema, db: AsyncSession, user: User):
    image = Images(**body.dict(), owner_id=user.id)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def get_all_images(limit: int, offset: int, db: AsyncSession, user_id: int):
    stmt = select(Images).filter_by(owner_id=user_id).offset(offset).limit(limit)
    result = await db.execute(stmt)
    images = result.scalars()
    return images


async def get_image_by_url(image_url: str, db: AsyncSession, user_id: int):
    stmt = select(Images).filter_by(images_url=image_url, owner_id=user_id)
    image = await db.execute(stmt)
    return image.scalar_one_or_none()


async def update_image_description(image_id: int, description: str, db: AsyncSession, user_id: int):
    stmt = select(Images).filter_by(id=image_id, owner_id=user_id)
    result = await db.execute(stmt)
    image = result.scalar_one_or_none()
    image.description = description
    await db.commit()
    await db.refresh(image)
    return image


async def delete_image(image_id: int, db: AsyncSession, user_id: int):
    stmt = select(Images).filter_by(id=image_id, owner_id=user_id)
    image = await db.execute(stmt)
    image = image.scalar_one_or_none()
    if image:
        await db.delete(image)
        await db.commit()
    return image
