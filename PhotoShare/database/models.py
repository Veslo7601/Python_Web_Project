from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean

Base = declarative_base()

class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String(32), nullable=True)
    images_id = Column(Integer, ForeignKey("images.id"))
    images = relationship("Images", back_populates="tags")

class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    image = Column(String(255), nullable=False)
    created_at = Column(Date, nullable=True)
    tag = relationship("Tags", back_populates="images", cascade="all, delete-orphan")