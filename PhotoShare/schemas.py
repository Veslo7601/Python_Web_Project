from datetime import datetime
from typing import Optional, List, Dict, Any, Type

from pydantic import BaseModel, Field, EmailStr, validator

from PhotoShare.database.models import Role


class UserSchema(BaseModel):
    username: str = Field(..., min_length=5, max_length=25)
    email: str = EmailStr
    password: str = Field(..., min_length=6, max_length=10)


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponseSchema(BaseModel):
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
    created_at: datetime = Field(None, format="iso")
    image_count: int | None

    class Config:
        from_attributes = True


class RequestEmailSchema(BaseModel):
    email: EmailStr


class TagSchemas(BaseModel):
    tag: Optional[str] = None


class TagResponseSchemas(TagSchemas):
    id: Optional[int] = None


class ImageSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    images_url: Optional[str] = None
    tags: Optional[List[TagSchemas]] = []


class ImageResponseSchema(BaseModel):
    id: int
    images_url: str
    title: str | None
    description: str | None
    tags: List[str] | None

    class Config:
        from_attributes = True

    @staticmethod
    def schema_extra(schema: Dict[str, Any], model: Type['ImageResponseSchema']) -> None:
        for prop in schema.get('properties', {}).values():
            prop.pop('title', None)

    @staticmethod
    def getter_dict(obj: Any) -> Dict[str, Any]:
        return {k: v.tag if k == 'tags' and isinstance(v, list) else v for k, v in obj.__dict__.items()}


class QRcodeResponseSchema(BaseModel):
    id: int
    images_url: str
    qr_code_url: str

    class Config:
        from_attributes = True
