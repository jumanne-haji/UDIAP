import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

@pytest.mark.asyncio
async def test_database_dialect_is_postgresql():
    assert settings.DATABASE_URL is not None
    engine = create_async_engine(settings.DATABASE_URL)
    dialect_name = engine.dialect.name
    print(f"\n[CI VERIFICATION] Active Database Dialect: {dialect_name}")
    assert dialect_name == "postgresql"
    await engine.dispose()

@pytest.mark.asyncio
async def test_redis_configuration_present():
    assert settings.REDIS_URL is not None
    assert settings.REDIS_URL.startswith("redis://")
