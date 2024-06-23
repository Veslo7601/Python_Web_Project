import enum
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, func, Enum
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String(32), nullable=True, unique=True)
    images_id = Column(Integer, ForeignKey("images.id"))
    images = relationship("Images", back_populates="tags")


class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment = Column(String(512), nullable=True)
    created_at = Column(Date, nullable=True)
    updated_at = Column(Date, nullable=True)
    images_id = Column(Integer, ForeignKey("images.id"))
    images = relationship("Images", back_populates="comments")


class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    image = Column(String(255), nullable=True)
    created_at = Column(Date, nullable=True)
    tags = relationship("Tags", back_populates="images", cascade="all, delete-orphan")
    comments = relationship("Comments", back_populates="images", cascade="all, delete-orphan")


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