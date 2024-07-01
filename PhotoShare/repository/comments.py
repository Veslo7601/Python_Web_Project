from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.models import Images, Comments

async def get_image_by_id_for_comments(image_id: int, db: AsyncSession,):
    stmt = select(Images).filter_by(id=image_id)
    image = await db.execute(stmt)
    return image.unique().scalar_one_or_none()

async def get_all_comments(image_id: int, limit: int, offset: int, db: AsyncSession):
    request = select(Comments).filter_by(images_id=image_id).offset(offset).limit(limit)
    comment = await db.execute(request)
    comment = comment.scalars()
    return comment

async def add_comment_to_image(image: Images, description: str, db: AsyncSession, user_id: int):
    comment = Comments(description=description, images_id=image.id, user_id = user_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(comment_id: int, db: AsyncSession):
    request = select(Comments).filter_by(id=comment_id)
    comment = await db.execute(request)
    comment = comment.scalar_one_or_none()
    if comment:
        await db.delete(comment)
        await db.commit()
    return comment

async def update_comment(comment_id: int, description: str, db: AsyncSession, user_id: int):
    request = select(Comments).filter_by(id=comment_id, user_id=user_id)
    comment = await db.execute(request)
    comment = comment.scalar_one_or_none()
    comment.description = description
    await db.commit()
    await db.refresh(comment)
    return comment