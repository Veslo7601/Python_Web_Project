import cloudinary
from cloudinary.uploader import upload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from fastapi import UploadFile, File, HTTPException
from datetime import datetime

from PhotoShare.conf.config import settings
from PhotoShare.database.models import User, Images, Tags
from PhotoShare.schemas import ImageSchema
from PhotoShare.services.qrcode import generate_qr_code


cloudinary.config(
    cloud_name=settings.CLD_NAME,
    api_key=settings.CLD_API_KEY,
    api_secret=settings.CLD_API_SECRET,
    secure=True,
)


async def add_image(
    title: Optional[str],
    description: Optional[str],
    tags: Optional[List[str]],
    file: UploadFile,
    user_id: int,
    db: AsyncSession
):
    try:
        upload_result = cloudinary.uploader.upload(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось загрузить изображение: {str(e)}")

    url = upload_result.get('secure_url')
    if not url:
        raise HTTPException(status_code=500, detail="Загрузка изображения не удалась, URL не найден")

    picture = Images(
        title=title,
        images_url=url,
        description=description,
        owner_id=user_id,
        created_at=datetime.now()
    )

    if tags:
        for tag_name in tags:
            result = await db.execute(select(Tags).filter(Tags.tag == tag_name))
            tag = result.scalar_one_or_none()
            if not tag:
                tag = Tags(tag=tag_name)
                db.add(tag)
                await db.commit()
                await db.refresh(tag)
            picture.tags.append(tag)

    db.add(picture)
    await db.commit()
    await db.refresh(picture)

    return picture


async def get_image(images_id: int, db: AsyncSession):
    result = await db.execute(select(Images).filter(Images.id == images_id))
    picture = result.scalar_one_or_none()
    return picture


async def get_all_images(limit: int, offset: int, db: AsyncSession, user_id: int):
    stmt = select(Images).filter(Images.owner_id == user_id).offset(offset).limit(limit)
    result = await db.execute(stmt)
    images = result.scalars().all()
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


async def delete_image(image_id: int, db: AsyncSession, user: User):
    stmt = select(Images).filter_by(id=image_id, owner_id=user.id)
    image = await db.execute(stmt)
    image = image.scalar_one_or_none()
    if image:
        await db.delete(image)
        user.image_count -= 1
        await db.commit()
    return image


async def update_image_qr_code(image_id: int, db: AsyncSession, user_id: int):
    result = await db.execute(select(Images).filter_by(id=image_id, owner_id=user_id))
    image = result.scalar_one_or_none()
    if image is None:
        return None

    qr_code_url = await generate_qr_code(image.images_url)
    image.qr_code_url = qr_code_url
    await db.commit()
    await db.refresh(image)
    return qr_code_url