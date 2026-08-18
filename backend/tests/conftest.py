import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

@pytest_asyncio.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()
