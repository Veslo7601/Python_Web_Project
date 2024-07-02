import contextlib

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from ..conf.config import settings


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False,
                                                                     bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except AttributeError as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.SQLALCHEMY_DATABASE_URL)


async def get_database():
    async with sessionmanager.session() as session:
        yield session
