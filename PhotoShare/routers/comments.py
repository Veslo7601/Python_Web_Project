
from typing import List
from fastapi import APIRouter, Depends,  HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from PhotoShare.database.database import get_database
from PhotoShare.schemas import CommentsResponseSchema
from PhotoShare.services.auth import auth_service
from PhotoShare.database.models import User, Role
from PhotoShare.services.role import RoleAccess

from PhotoShare.repository import comments as repositories_comments




access_to_route_all = RoleAccess([Role.admin, Role.moderator])

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/{image_id}", response_model=List[CommentsResponseSchema])
async def get_all_comments(image_id: int,
                          limit: int = Query(10, ge=10, le=500),
                          offset: int = Query(0, ge=0),
                          db: AsyncSession = Depends(get_database),
                          ):
    comments = await repositories_comments.get_all_comments(image_id, limit, offset, db)
    if comments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comments


@router.post("/{image_id}", response_model=CommentsResponseSchema)
async def add_comment_to_image(image_id: int,
                               description: str,
                               user: User = Depends(auth_service.get_current_user),
                               db: AsyncSession = Depends(get_database)):

    image = await repositories_comments.get_image_by_id_for_comments(image_id, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    comment = await repositories_comments.add_comment_to_image(image, description, db, user.id)
    return comment


@router.delete("/{comment_id}", response_model=CommentsResponseSchema, dependencies=[Depends(access_to_route_all)])
async def delete_comment(comment_id: int,
                         db = Depends(get_database)):
    comment = await repositories_comments.delete_comment(comment_id, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=CommentsResponseSchema)
async def update_comment(comment_id: int,
                         description: str,
                         user: User = Depends(auth_service.get_current_user),
                         db: AsyncSession = Depends(get_database)):
    comment = await repositories_comments.update_comment(comment_id, description, db, user.id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment