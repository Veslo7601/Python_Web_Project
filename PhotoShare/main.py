import uvicorn
import os
import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from PhotoShare.database.database import get_database
from PhotoShare.routers import auth, users, images, tags, comments
from PhotoShare.conf.config import settings

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(images.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(comments.router, prefix="/api")

# @app.on_event("startup")
# async def startup():
#     r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
#     await FastAPILimiter.init(r)


@app.get("/")
def index():
    """
    Root endpoint to check if the app is up and running.

    Returns:
        dict: A dictionary with a message indicating that the app running.

    """

    return {"message": "Hello world"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_database)):
    """
    Healthchecker to check if the app is up and running database connection.

    Args:
        db (AsyncSession): Database session

    Raises:
        HTTPException: If there is an error connecting to the database.

    Returns:
        dict: A dictionary with a message indicating that the app is up and running.

    """
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
