"""
Tests for database operations
"""
import pytest
from kopi_bot.database import DatabaseService
from kopi_bot.models import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool


@pytest.fixture
async def test_db_service():
    """Create a test database service"""
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
    
    # Create database service
    db_service = DatabaseService()
    db_service.async_engine = engine
    db_service.async_session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    yield db_service
    
    # Cleanup
    await engine.dispose()


@pytest.mark.asyncio
class TestDatabaseService:
    """Test database service operations"""
    
    async def test_create_conversation(self, test_db_service):
        """Test creating a new conversation"""
        conversation_id = await test_db_service.create_conversation(
            topic="climate change",
            bot_position="strongly_for"
        )
        
        assert conversation_id is not None
        assert len(conversation_id) > 0
        assert isinstance(conversation_id, str)
    
    async def test_add_message(self, test_db_service):
        """Test adding messages to a conversation"""
        # Create conversation first
        conversation_id = await test_db_service.create_conversation(
            topic="test topic",
            bot_position="for"
        )
        
        # Add user message
        await test_db_service.add_message(conversation_id, "user", "Test user message")
        
        # Add bot message
        await test_db_service.add_message(conversation_id, "bot", "Test bot response")
        
        # Verify messages were added
        messages = await test_db_service.get_conversation_messages(conversation_id)
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[0]["message"] == "Test user message"
        assert messages[1]["role"] == "bot"
        assert messages[1]["message"] == "Test bot response"
    
    async def test_get_conversation_messages(self, test_db_service):
        """Test retrieving conversation messages"""
        # Create conversation and add messages
        conversation_id = await test_db_service.create_conversation(
            topic="test topic",
            bot_position="for"
        )
        
        messages_to_add = [
            ("user", "Message 1"),
            ("bot", "Response 1"),
            ("user", "Message 2"),
            ("bot", "Response 2"),
            ("user", "Message 3"),
            ("bot", "Response 3")
        ]
        
        for role, content in messages_to_add:
            await test_db_service.add_message(conversation_id, role, content)
        
        # Get messages with limit
        messages = await test_db_service.get_conversation_messages(conversation_id, limit=4)
        assert len(messages) == 4
        
        # Should be in chronological order
        assert messages[0]["message"] == "Message 2"  # Oldest in the returned set
        assert messages[-1]["message"] == "Response 3"  # Most recent
    
    async def test_conversation_exists(self, test_db_service):
        """Test checking if conversation exists"""
        # Test non-existent conversation
        exists = await test_db_service.conversation_exists("non-existent-id")
        assert exists is False
        
        # Create conversation
        conversation_id = await test_db_service.create_conversation(
            topic="test topic",
            bot_position="for"
        )
        
        # Test existing conversation
        exists = await test_db_service.conversation_exists(conversation_id)
        assert exists is True
    
    async def test_get_conversation_topic(self, test_db_service):
        """Test retrieving conversation topic and bot position"""
        # Test non-existent conversation
        topic_info = await test_db_service.get_conversation_topic("non-existent-id")
        assert topic_info is None
        
        # Create conversation
        conversation_id = await test_db_service.create_conversation(
            topic="climate change",
            bot_position="strongly_for"
        )
        
        # Get topic info
        topic_info = await test_db_service.get_conversation_topic(conversation_id)
        assert topic_info is not None
        assert topic_info["topic"] == "climate change"
        assert topic_info["bot_position"] == "strongly_for"
    
    async def test_get_conversation_messages_empty(self, test_db_service):
        """Test retrieving messages from non-existent conversation"""
        messages = await test_db_service.get_conversation_messages("non-existent-id")
        assert messages == []
    
    async def test_message_ordering(self, test_db_service):
        """Test that messages are returned in correct chronological order"""
        # Create conversation
        conversation_id = await test_db_service.create_conversation(
            topic="test topic",
            bot_position="for"
        )
        
        # Add messages in sequence
        messages_sequence = [
            ("user", "First user message"),
            ("bot", "First bot response"),
            ("user", "Second user message"),
            ("bot", "Second bot response")
        ]
        
        for role, content in messages_sequence:
            await test_db_service.add_message(conversation_id, role, content)
            # Small delay to ensure different timestamps
            import asyncio
            await asyncio.sleep(0.001)
        
        # Retrieve messages
        messages = await test_db_service.get_conversation_messages(conversation_id)
        
        # Verify order
        assert len(messages) == 4
        assert messages[0]["message"] == "First user message"
        assert messages[1]["message"] == "First bot response"
        assert messages[2]["message"] == "Second user message"
        assert messages[3]["message"] == "Second bot response"
    
    async def test_conversation_limit(self, test_db_service):
        """Test message limit functionality"""
        # Create conversation
        conversation_id = await test_db_service.create_conversation(
            topic="test topic",
            bot_position="for"
        )
        
        # Add many messages
        for i in range(10):
            await test_db_service.add_message(conversation_id, "user", f"User message {i}")
            await test_db_service.add_message(conversation_id, "bot", f"Bot response {i}")
        
        # Test limit
        messages = await test_db_service.get_conversation_messages(conversation_id, limit=5)
        assert len(messages) == 5
        
        # Should be the most recent 5 messages
        assert "message 7" in messages[0]["message"].lower() or "response 7" in messages[0]["message"].lower()
        assert "response 9" in messages[-1]["message"].lower()