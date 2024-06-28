from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.models import User, Images, Comments
from PhotoShare.schemas import ImageSchema

async def add_comment_to_image(image: Images, description: str, db: AsyncSession, user_id: int):
    comment = Comments(description=description, images_id=image.id, user_id = user_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)


async def delete_comment(comment_id: isinstance, db: AsyncSession, user_id: int):
    request = select(Comments).filter_by(id=comment_id)
    comment = await db.execute(request)
    comment = comment.scalar_one_or_none()
    if comment:
        await db.delete(comment)
        await db.commit()
    return comment
