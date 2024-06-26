from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from PhotoShare.database.models import Role


class UserSchema(BaseModel):
    username: str = Field(..., min_length=5, max_length=25)
    email: str = EmailStr
    password: str = Field(..., min_length=6, max_length=10)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str | None
    role: Role | None

    class Config:
        from_attributes = True


class UserResponseSchemaForAdmin(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str | None
    role: Role | None
    created_at: str
    image_count: int

    class Config:
        from_attributes = True


class RequestEmailSchema(BaseModel):
    email: EmailStr


class ImageSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    images_url: Optional[str] = None


class ImageResponseSchema(BaseModel):
    id: int
    images_url: str
    title: str | None
    description: str | None

    class Config:
        from_attributes = True
