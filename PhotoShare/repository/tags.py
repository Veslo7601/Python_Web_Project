from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from PhotoShare.database.models import Tags
from PhotoShare.schemas import TagSchemas


async def create_tag_in_db(body: TagSchemas, db: AsyncSession):
    """
    Create new tag in database

    :param body: TagSchemas
    :param db: AsyncSession
    :return: TagSchemas
    """

    result = await db.execute(select(Tags).filter(Tags.tag == body.tag))
    existing_tag = result.scalar()
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag already created")

    tag = Tags(tag=body.tag)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def get_all_tags(skip: int, limit: int, db: AsyncSession):
    """
    Get all tags from database

    :param skip: int
    :param limit: int
    :param db: AsyncSession
    :return: List[TagSchemas]
    """

    smtp = select(Tags).offset(skip).limit(limit)
    result = await db.execute(smtp)
    images = result.scalars()
    return images


async def update_tag(tag_id: int, body: TagSchemas, db: AsyncSession):
    """
    Update tag in database

    :param tag_id: int
    :param body: TagSchemas
    :param db: AsyncSession
    :return: TagSchemas
    """

    result = await db.execute(select(Tags).filter(Tags.id == tag_id))
    tag = result.scalar()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.tag = body.tag
    await db.commit()
    await db.refresh(tag)
    return tag


async def remove_tag(tag_id: int, db: AsyncSession):
    """
    Remove tag from database

    :param tag_id: int
    :param db: AsyncSession
    :return: TagSchemas
    """

    result = await db.execute(select(Tags).filter(Tags.id == tag_id))
    tag = result.scalar()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    await db.delete(tag)
    await db.commit()
    return tag
