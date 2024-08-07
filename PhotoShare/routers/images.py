from pathlib import Path
from typing import List

import cloudinary.uploader
from fastapi import APIRouter, Depends, status, File, UploadFile, Form, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.conf.config import settings
from PhotoShare.database.database import get_database
from PhotoShare.database.models import User
from PhotoShare.schemas import ImageSchema, ImageResponseSchema, QRcodeResponseSchema, ImageResponseUpdateSchema
from PhotoShare.services.auth import auth_service
from PhotoShare.services.images import build_transform_url
from PhotoShare.repository.images import add_image, get_all_images, get_image_by_url, update_image_description, delete_image, update_image_qr_code, update_image_url, get_image_by_id

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
        tags: List[str] = Form([]),
        db: AsyncSession = Depends(get_database),
        user: User = Depends(auth_service.get_current_user)
):
    """
    Create new image

    :param title: str
    :param description: str
    :param file: UploadFile
    :param tags: List[str]
    :param db: AsyncSession
    :param user: User
    :return: ImageSchema
    """

    public_id = f"users/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )

    body = ImageSchema(title=title, description=description, images_url=res_url)

    image = await add_image(body, tags, db, user)
    return image


@router.get(
    "/images", response_model=List[ImageResponseSchema], status_code=status.HTTP_200_OK
)
async def get_images(
        limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)
):
    """
    Get all images from database

    :param limit: int
    :param offset: int
    :param db: AsyncSession
    :param user: User
    :return: List[ImageSchema]
    """

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
    """
    Get image by url from database

    :param image_path: str
    :param db: AsyncSession
    :param user: User
    :return: ImageSchema
    """

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
    """
    Edit image description

    :param description: str
    :param image_id: int
    :param db: AsyncSession
    :param user: User
    :return: ImageSchema
    """

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
    """
    Remove image from database

    :param image_id: int
    :param db: AsyncSession
    :param user: User
    :return: None
    """

    image = await delete_image(image_id, db, user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.put(
    "/{image_id}/generate_qr", response_model=QRcodeResponseSchema
)
async def generate_qr_for_image(
        image_id: int = Path(ge=1),
        db: AsyncSession = Depends(get_database), user: User = Depends(auth_service.get_current_user)
):
    """
    Generate QR code for image

    :param image_id: int
    :param db: AsyncSession
    :param user: User
    :return: QRcodeResponseSchema
    """

    try:
        qr_code_url = await update_image_qr_code(image_id, db, user.id)

        if qr_code_url is None:
            raise HTTPException(status_code=404, detail="Image not found")

        return {
            "id": image_id,
            "qr_code_url": qr_code_url
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{image_id}/transform", response_model=ImageResponseUpdateSchema)
async def transform_image(
        image_id: int = Path(ge=1),
        width: int = Query(default=250),
        height: int = Query(default=250),
        crop: str = Query(default="fill"),
        filter: str = Query(default="grayscale",
                            description="Possible values: art:zorro, art:al_dente, art:hokusai, art:peacock, cartoonify"),
        db: AsyncSession = Depends(get_database),
        user: User = Depends(auth_service.get_current_user)

):
    """
    Transform image

    :param image_id: int
    :param width: int
    :param height: int
    :param crop: str
    :param filter: str
    :param db: AsyncSession
    :param user: User
    :return: ImageSchema
    """

    image = await get_image_by_id(image_id, db, user.id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    url = await build_transform_url(user, width, height, crop, filter)
    image = await update_image_url(image_id, db, user, url)

    return image
