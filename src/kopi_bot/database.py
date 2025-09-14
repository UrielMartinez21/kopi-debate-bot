"""
Database service for managing conversations and messages
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import List, Optional
from .models import Base, Conversation, Message
from .config import settings
import uuid


class DatabaseService:
    """Database service for conversation management"""
    
    def __init__(self):
        # Use async engine for better performance
        if settings.database_url.startswith("postgresql"):
            # For PostgreSQL, use asyncpg
            async_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
            self.async_engine = create_async_engine(async_url, echo=settings.debug)
        else:
            # For SQLite, use aiosqlite  
            async_url = settings.database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
            self.async_engine = create_async_engine(async_url, echo=settings.debug)
        
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Sync engine for migrations and setup
        self.sync_engine = create_engine(settings.database_url, echo=settings.debug)
        self.sync_session_factory = sessionmaker(bind=self.sync_engine)
    
    async def create_tables(self):
        """Create database tables"""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def create_conversation(self, topic: str, bot_position: str) -> str:
        """Create a new conversation and return its ID"""
        conversation_id = str(uuid.uuid4())
        
        async with self.async_session_factory() as session:
            conversation = Conversation(
                id=conversation_id,
                topic=topic,
                bot_position=bot_position
            )
            session.add(conversation)
            await session.commit()
            
        return conversation_id
    
    async def add_message(self, conversation_id: str, role: str, content: str) -> None:
        """Add a message to a conversation"""
        async with self.async_session_factory() as session:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content
            )
            session.add(message)
            await session.commit()
    
    async def get_conversation_messages(self, conversation_id: str, limit: int = 10) -> List[dict]:
        """Get recent messages from a conversation"""
        async with self.async_session_factory() as session:
            # Get conversation to ensure it exists
            conversation = await session.get(Conversation, conversation_id)
            if not conversation:
                return []
            
            # Get recent messages
            from sqlalchemy import select, desc
            
            query = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(desc(Message.created_at))
                .limit(limit)
            )
            
            result = await session.execute(query)
            messages = result.scalars().all()
            
            # Convert to dict format and reverse to get chronological order
            message_dicts = []
            for message in reversed(messages):
                message_dicts.append({
                    "role": message.role,
                    "message": message.content
                })
            
            return message_dicts
    
    async def conversation_exists(self, conversation_id: str) -> bool:
        """Check if a conversation exists"""
        async with self.async_session_factory() as session:
            conversation = await session.get(Conversation, conversation_id)
            return conversation is not None
    
    async def get_conversation_topic(self, conversation_id: str) -> Optional[dict]:
        """Get conversation topic and bot position"""
        async with self.async_session_factory() as session:
            conversation = await session.get(Conversation, conversation_id)
            if not conversation:
                return None
            
            return {
                "topic": conversation.topic,
                "bot_position": conversation.bot_position
            }
    
    async def close(self):
        """Close database connections"""
        await self.async_engine.dispose()


# Global database service instance
db_service = DatabaseService()