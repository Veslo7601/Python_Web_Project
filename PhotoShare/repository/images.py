from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from PhotoShare.database.models import User, Images, Tags
from PhotoShare.schemas import ImageSchema

from PhotoShare.services.qrcode import generate_qr_code


async def add_image(body: ImageSchema, tags: Optional[List[str]], db: AsyncSession, user: User):
    try:
        image = Images(title=body.title, description=body.description, images_url=body.images_url, owner_id=user.id)

        if tags:
            result = await db.execute(select(Tags).filter(Tags.tag.in_(tags)))
            db_tags = result.scalars().all()
            if db_tags:
                for tag in db_tags:
                    image.tags.append(tag)

            elif db_tags is None:
                for tag_name in tags:
                    db_tag = Tags(tag=tag_name)
                    image.tags.append(db_tag)

        db.add(image)
        user.image_count += 1
        await db.commit()
        await db.refresh(image)
        result = await db.execute(select(Images).options(joinedload(Images.tags)).filter_by(id=image.id))
        image = result.unique().scalar_one_or_none()

        if image:
            tag_names = [tag.tag for tag in image.tags]

            image_dict = {'id': image.id, 'images_url': image.images_url, 'title': image.title,
                          'description': image.description, 'tags': tag_names}
            return image_dict

    except Exception as e:
        await db.rollback()
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to upload image: {str(e)}")


async def get_all_images(limit: int, offset: int, db: AsyncSession, user_id: int):
    stmt = select(Images).filter_by(owner_id=user_id).offset(offset).limit(limit)
    result = await db.execute(stmt)
    images = result.scalars()
    return images


async def get_image_by_url(image_url: str, db: AsyncSession, user_id: int):
    stmt = select(Images).options(joinedload(Images.tags)).filter_by(images_url=image_url, owner_id=user_id)
    result = await db.execute(stmt)
    image = result.unique().scalar_one_or_none()

    if image:
        tag_names = [tag.tag for tag in image.tags]

        image_dict = {
            'id': image.id,
            'images_url': image.images_url,
            'title': image.title,
            'description': image.description,
            'tags': tag_names
        }

        return image_dict


async def get_image_by_id(image_id: int, db: AsyncSession, user_id: int):
    stmt = select(Images).filter_by(id=image_id, owner_id=user_id)
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


async def update_image_url(image_id: int, db: AsyncSession, user: User, transformed_url: str):
    result = await db.execute(select(Images).filter_by(id=image_id, owner_id=user.id))
    image = result.scalar_one_or_none()
    image.images_url = transformed_url
    await db.commit()
    await db.refresh(image)
    return image
