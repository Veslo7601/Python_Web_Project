from pathlib import Path

import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from PhotoShare.database.database import get_database
from PhotoShare.schemas import UserResponseSchema, UserResponseSchemaForAdmin
from PhotoShare.services.auth import auth_service
from PhotoShare.database.models import User, Role
from PhotoShare.repository import users as repositories_user
from PhotoShare.services.role import RoleAccess

router = APIRouter(prefix="/users", tags=["users"])

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLD_NAME'),
    api_key=os.getenv('CLD_API_KEY'),
    api_secret=os.getenv('CLD_API_SECRET'),
    secure=True,
)

access_to_route_all = RoleAccess([Role.admin])


@router.get(
    "/{username}",
    response_model=UserResponseSchemaForAdmin,
    dependencies=[Depends(access_to_route_all)],
)
async def get_user_info(username: str = Path()):
    user_info = await repositories_user.get_user_by_username(username)
    return user_info


@router.get(
    "/me",
    response_model=UserResponseSchema,
    dependencies=[Depends(RateLimiter(times=4, seconds=30))],
)
async def get_user(user: User = Depends(auth_service.get_current_user)):
    return user


@router.patch(
    "/avatar",
    response_model=UserResponseSchema,
    dependencies=[Depends(RateLimiter(times=4, seconds=30))],
)
async def get_avatar(
    file: UploadFile = File(),
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_database),
):
    public_id = f"Web21/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=100, height=150, crop="fill", version=res.get("version")
    )
    user = await repositories_user.update_avatar_url(user.email, res_url, db)
    return user