from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.database import get_database
from PhotoShare.schemas import TagResponseSchemas, TagSchemas
from PhotoShare.repository.tags import get_all_tags, create_tag_in_db, update_tag, remove_tag


router = APIRouter(prefix='/tags', tags=["tags"])


@router.post("/create_tag", response_model=TagResponseSchemas, status_code=status.HTTP_201_CREATED)
async def create_tag(body: TagSchemas, db: AsyncSession = Depends(get_database)):
    result = await create_tag_in_db(body, db)
    return result


@router.get("/get_all_tags", response_model=List[TagResponseSchemas], status_code=status.HTTP_200_OK)
async def get_tags(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_database)):
    tags = await get_all_tags(skip, limit, db)
    return tags


@router.put("/update_tag/{tag_id}", response_model=TagResponseSchemas, status_code=status.HTTP_200_OK)
async def update_tag_endpoint(tag_id: int, body: TagSchemas, db: AsyncSession = Depends(get_database)):
    result = await update_tag(tag_id, body, db)
    return result


@router.delete("/delete_tag/{tag_id}", response_model=TagResponseSchemas, status_code=status.HTTP_200_OK)
async def remove_tag_endpoint(tag_id: int, db: AsyncSession = Depends(get_database)):
    result = await remove_tag(tag_id, db)
    return result
