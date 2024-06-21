from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean

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