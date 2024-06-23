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
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now(), nullable=True)

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    tags: Mapped["Tags"] = relationship("Tags", backref="images", cascade="all, delete-orphan")
    comments: Mapped["Comments"] = relationship("Comments", backref="images", cascade="all, delete-orphan")


class Tags(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str] = mapped_column(String(25), nullable=True, unique=True)
    images_id: Mapped[int] = mapped_column(ForeignKey("images.id"), nullable=True)
    images: Mapped["Images"] = relationship("Images", backref="tags", lazy="joined")


class Comments(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    images_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE", onupdate="CASCADE")
    )


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(75), nullable=False, unique=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    role: Mapped[Enum] = mapped_column("role", Enum(Role), default=Role.user, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    blocked: Mapped[bool] = mapped_column(default=False)