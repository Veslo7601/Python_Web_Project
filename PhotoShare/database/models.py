import enum
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, ForeignKey, Boolean, func, Enum
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class Images(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    images_url: Mapped[str] = mapped_column(String(255))
    qr_code_url: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now(), nullable=True)

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    tags: Mapped[list["Tags"]] = relationship("Tags", back_populates="images", cascade="all, delete-orphan")
    comments: Mapped["Comments"] = relationship("Comments", back_populates="images", cascade="all, delete-orphan")


class Tags(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str] = mapped_column(String(25), nullable=True, unique=True)
    images_id: Mapped[int] = mapped_column(ForeignKey("images.id"), nullable=True)
    images: Mapped["Images"] = relationship("Images", back_populates="tags", lazy="joined")


class Comments(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255))

    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    images_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    images: Mapped["Images"] = relationship("Images", back_populates="comments")


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(75), nullable=False, unique=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    role: Mapped[Enum] = mapped_column("role", Enum(Role), default=Role.user, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    blocked: Mapped[bool] = mapped_column(default=False)
    image_count: Mapped[int] = mapped_column("image_count", default=0, nullable=True)
