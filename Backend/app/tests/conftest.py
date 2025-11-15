import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.api.deps import get_db
from alembic import command
from alembic.config import Config
from app.core.config import settings
import app

engine_test = create_async_engine(settings.database_test_url, echo=False)
SessionTest = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="session", autouse=True)
def apply_migrations_in_db_test():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_test_url)
    command.upgrade(alembic_cfg, "head")

@pytest.fixture()
async def db_session():
    async with engine_test.begin() as conn:
        await conn.begin()
        await conn.begin_nested()
        async_session = SessionTest(bind=conn)
        try:
            yield async_session
        finally:
            await async_session.close()
            await conn.rollback()

async def override_get_db():
    async with SessionTest() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db