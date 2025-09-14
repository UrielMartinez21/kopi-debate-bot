"""
Pytest configuration and fixtures
"""
import pytest
import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from kopi_bot.main import app
from kopi_bot.models import Base
from kopi_bot.database import db_service


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncGenerator[None, None]:
    """Create a test database for each test."""
    # Use in-memory SQLite for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Replace the global db service engine with test engine
    original_engine = db_service.async_engine
    original_session_factory = db_service.async_session_factory
    
    db_service.async_engine = engine
    db_service.async_session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    yield
    
    # Cleanup
    await engine.dispose()
    db_service.async_engine = original_engine
    db_service.async_session_factory = original_session_factory


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_conversation_request():
    """Sample conversation request for testing."""
    return {
        "conversation_id": None,
        "message": "I think climate change is not real and it's just a hoax"
    }


@pytest.fixture
def sample_continue_request():
    """Sample request to continue conversation."""
    return {
        "conversation_id": "test-conv-id",
        "message": "But what about the natural climate cycles?"
    }