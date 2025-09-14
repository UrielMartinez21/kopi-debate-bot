"""
Main FastAPI application for the Kopi Debate Bot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog
from typing import Dict, Any
import time

from .schemas import ConversationRequest, ConversationResponse, MessageData, MessageRole
from .database import db_service
from .debate_bot import DebateBot
from .config import settings

# Setup structured logging
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup
    logger.info("Starting Kopi Debate Bot API")
    await db_service.create_tables()
    yield
    # Shutdown
    logger.info("Shutting down Kopi Debate Bot API")
    await db_service.close()


# Create FastAPI app with lifespan management
app = FastAPI(
    title=settings.app_name,
    description="A persuasive AI chatbot that maintains firm debate positions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize debate bot
debate_bot = DebateBot()


@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Ensure response time is under 30 seconds (requirement)
    if process_time > 30:
        logger.warning("Response time exceeded 30 seconds", process_time=process_time)
    
    return response


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Kopi Debate Bot API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "debug_mode": settings.debug,
        "timestamp": time.time()
    }


@app.post("/conversation", response_model=ConversationResponse)
async def handle_conversation(request: ConversationRequest) -> ConversationResponse:
    """
    Handle conversation messages and return bot responses
    
    This is the main endpoint that:
    1. Creates new conversations when conversation_id is null
    2. Continues existing conversations when conversation_id is provided
    3. Returns the conversation history with the bot's response
    """
    try:
        logger.info("Processing conversation request", 
                   conversation_id=request.conversation_id,
                   message_length=len(request.message))
        
        if request.conversation_id is None:
            # New conversation - analyze topic and determine bot stance
            logger.info("Starting new conversation")
            topic, debate_topic = debate_bot.analyze_first_message(request.message)
            
            # Create new conversation in database
            conversation_id = await db_service.create_conversation(
                topic=topic,
                bot_position=debate_topic.stance.value
            )
            
            # Add user's first message
            await db_service.add_message(conversation_id, "user", request.message)
            
            # Generate bot's response
            bot_response = debate_bot.generate_response(
                request.message, 
                [], 
                debate_topic
            )
            
            # Add bot's response to database
            await db_service.add_message(conversation_id, "bot", bot_response)
            
            # Prepare response
            messages = [
                MessageData(role=MessageRole.USER, message=request.message),
                MessageData(role=MessageRole.BOT, message=bot_response)
            ]
            
        else:
            # Existing conversation
            logger.info("Continuing existing conversation", 
                       conversation_id=request.conversation_id)
            
            # Check if conversation exists
            if not await db_service.conversation_exists(request.conversation_id):
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found"
                )
            
            # Get conversation topic and bot position
            conversation_info = await db_service.get_conversation_topic(request.conversation_id)
            if not conversation_info:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation topic not found"
                )
            
            # Get conversation history
            conversation_history = await db_service.get_conversation_messages(
                request.conversation_id,
                limit=settings.max_conversation_history * 2  # User + bot messages
            )
            
            # Recreate debate topic from stored info
            from .debate_bot import DebateStance
            stance = DebateStance(conversation_info["bot_position"])
            debate_topic = debate_bot._create_debate_topic(conversation_info["topic"], stance)
            
            # Add user's new message
            await db_service.add_message(request.conversation_id, "user", request.message)
            
            # Generate bot response based on history
            bot_response = debate_bot.generate_response(
                request.message,
                conversation_history,
                debate_topic
            )
            
            # Add bot's response
            await db_service.add_message(request.conversation_id, "bot", bot_response)
            
            # Get updated conversation history (last 5 messages from each side)
            recent_messages = await db_service.get_conversation_messages(
                request.conversation_id,
                limit=settings.max_conversation_history * 2
            )
            
            # Convert to MessageData objects
            messages = []
            for msg in recent_messages:
                role = MessageRole.USER if msg["role"] == "user" else MessageRole.BOT
                messages.append(MessageData(role=role, message=msg["message"]))
            
            conversation_id = request.conversation_id
        
        logger.info("Successfully processed conversation", 
                   conversation_id=conversation_id,
                   response_length=len(messages[-1].message) if messages else 0)
        
        return ConversationResponse(
            conversation_id=conversation_id,
            messages=messages
        )
        
    except Exception as e:
        logger.error("Error processing conversation", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred while processing conversation"
        )


@app.get("/conversation/{conversation_id}")
async def get_conversation_history(conversation_id: str) -> Dict[str, Any]:
    """Get conversation history for debugging purposes"""
    if not await db_service.conversation_exists(conversation_id):
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    
    messages = await db_service.get_conversation_messages(conversation_id, limit=50)
    conversation_info = await db_service.get_conversation_topic(conversation_id)
    
    return {
        "conversation_id": conversation_id,
        "topic": conversation_info["topic"] if conversation_info else None,
        "bot_position": conversation_info["bot_position"] if conversation_info else None,
        "messages": messages,
        "message_count": len(messages)
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )