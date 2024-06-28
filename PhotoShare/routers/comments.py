
from fastapi import APIRouter, Depends,  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from PhotoShare.database.database import get_database
from PhotoShare.schemas import CommentsResponseSchema
from PhotoShare.services.auth import auth_service
from PhotoShare.database.models import User, Role
from PhotoShare.repository import users as repositories_user
from PhotoShare.services.role import RoleAccess

from PhotoShare.repository import comments as repositories_comments
from PhotoShare.repository import images as repositories_images

access_to_route_all = RoleAccess([Role.admin, Role.moderator])

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/id/{image_id}",
             response_model=str)
async def add_comment_to_image(image_id: int,
                               description: str,
                               user: User = Depends(auth_service.get_current_user),
                               db: AsyncSession = Depends(get_database)):

    image = await repositories_images.get_image_by_id(image_id, db, user.id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    await repositories_comments.add_comment_to_image(image, description, db, user.id)
    return f"Comment {description} add"

@router.delete("/{comment_id}",
               response_model=str,
               dependencies=[Depends(access_to_route_all)])
async def delete_comment(comment_id: int,
                         user: User = Depends(auth_service.get_current_user),
                         db = Depends(get_database)):
    comment = await repositories_comments.delete_comment(comment_id, db, user.id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return f"Comment delete"