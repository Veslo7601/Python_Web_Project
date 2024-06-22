from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, func
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

class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    role = Column(String(64), nullable=True, unique=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)