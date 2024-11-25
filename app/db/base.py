from typing import AsyncGenerator
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from settings.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, TEST_DB_NAME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData


class DatabaseManager:
    def __init__(self, db_url: str, sync_db_url: str):
        self.db_url = db_url
        self.sync_db_url = sync_db_url
        self.metadata = MetaData()
        self.Base = declarative_base(metadata=self.metadata)
        self.engine = create_async_engine(self.db_url)
        self.async_session_maker = async_sessionmaker(
            self.engine, expire_on_commit=False)

        if not database_exists(self.sync_db_url):
            create_database(self.sync_db_url)

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session

    async def get_session(self) -> AsyncSession:
        return self.async_session_maker()


main_db_manager = DatabaseManager(
    db_url=f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    sync_db_url=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
test_db_manager = DatabaseManager(
    db_url=f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}",
    sync_db_url=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)


async def init_all():
    await main_db_manager.init_models()
    await test_db_manager.init_models()
