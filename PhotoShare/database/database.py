from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
#DATABASE_URL = environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_database():
    """Create database"""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()