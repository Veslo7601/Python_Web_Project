from pathlib import Path
from typing import List, Optional
import cloudinary.uploader
from fastapi import APIRouter, Depends, status, File, UploadFile, Query, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.conf.config import settings
from PhotoShare.database.database import get_database
from PhotoShare.database.models import User, Images
from PhotoShare.schemas import ImageSchema, ImageResponseSchema
from PhotoShare.services.auth import auth_service
from PhotoShare.repository.images import add_image, get_image_by_url, update_image_description, delete_image, \
    update_image_qr_code, get_all_images, get_image

router = APIRouter(prefix="/image", tags=["images"])

cloudinary.config(
    cloud_name=settings.CLD_NAME,
    api_key=settings.CLD_API_KEY,
    api_secret=settings.CLD_API_SECRET,
    secure=True,
)


@router.post("/create_images", response_model=ImageResponseSchema, status_code=status.HTTP_201_CREATED)
async def post_picture(
    title: Optional[str] = Form(...),
    file: UploadFile = File(...),
    description: Optional[str] = Form(...),
    tags: List[str] = Form([]),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_database)
):
    tags_list = tags[0].split(",")[:5] if tags else []
    picture = await add_image(title, description, tags_list, file, current_user.id, db)
    return picture


@router.put(
    "/{image_id}", response_model=ImageResponseSchema
)
async def edit_image_description(
        description: str,
        image_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)
):
    image = await update_image_description(image_id, description, db, user.id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return image


@router.delete(
    "/{image_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def remove_image(
        image_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_database),
        user: User = Depends(auth_service.get_current_user)

):
    image = await delete_image(image_id, db, user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.put(
    "/{image_id}/generate_qr", response_model=str
)
async def generate_qr_for_image(
        image_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)
):
    qr_code_url = await update_image_qr_code(image_id, db, user.id)
    if qr_code_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return qr_code_url