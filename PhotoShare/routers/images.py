from pathlib import Path
from typing import List

import cloudinary.uploader
from fastapi import APIRouter, Depends, status, File, UploadFile, Form, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.conf.config import settings
from PhotoShare.database.database import get_database
from PhotoShare.database.models import User
from PhotoShare.schemas import ImageSchema, ImageResponseSchema
from PhotoShare.services.auth import auth_service
from PhotoShare.services.images import build_transform_url
from PhotoShare.repository.images import add_image, get_all_images, get_image_by_url, update_image_description, delete_image, update_image_qr_code, update_image_url, get_image_by_id

import qrcode
import qrcode.image.svg
from io import BytesIO
from fastapi.responses import StreamingResponse, JSONResponse

router = APIRouter(prefix="/image", tags=["images"])

cloudinary.config(
    cloud_name=settings.CLD_NAME,
    api_key=settings.CLD_API_KEY,
    api_secret=settings.CLD_API_SECRET,
    secure=True,
)


@router.post(
    "/", response_model=ImageResponseSchema, status_code=status.HTTP_201_CREATED
)
async def post_image(
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(),
        db: AsyncSession = Depends(get_database),
        user: User = Depends(auth_service.get_current_user)
):
    public_id = f"users/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )

    body = ImageSchema(title=title, description=description, images_url=res_url)

    image = await add_image(body, db, user)
    return image


@router.get(
    "/images", response_model=List[ImageResponseSchema], status_code=status.HTTP_200_OK
)
async def get_images(
        limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)
):
    images = await get_all_images(limit, offset, db, user.id)
    if images is None:
        return []
    return images


@router.get(
    "/", response_model=ImageResponseSchema, status_code=status.HTTP_200_OK
)
async def get_image(
        image_path: str,
        db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)
):
    image = await get_image_by_url(image_path, db, user.id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


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


@router.put("/{image_id}/transform", response_model=ImageResponseSchema)
async def transform_image(
        image_id: int = Path(ge=1),
        width: int = Query(default=250),
        height: int = Query(default=250),
        crop: str = Query(default="fill"),
        filter: str = Query(default=None),
        db: AsyncSession = Depends(get_database),
        user: User = Depends(auth_service.get_current_user)

):
    image = await get_image_by_id(image_id, db, user.id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    url = await build_transform_url(user, width, height, crop, filter)
    image = await update_image_url(image_id, db, user, url)

    return image
