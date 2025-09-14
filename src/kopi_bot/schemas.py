"""
Pydantic models for request and response schemas
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class MessageRole(str, Enum):
    """Message roles in the conversation"""
    USER = "user"
    BOT = "bot"


class MessageData(BaseModel):
    """Individual message data"""
    role: MessageRole
    message: str = Field(..., min_length=1, max_length=2000)


class ConversationRequest(BaseModel):
    """Request schema for conversation endpoint"""
    conversation_id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=2000)


class ConversationResponse(BaseModel):
    """Response schema for conversation endpoint"""
    conversation_id: str
    messages: List[MessageData] = Field(..., max_items=10)

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_123abc",
                "messages": [
                    {
                        "role": "user",
                        "message": "I think climate change is not real"
                    },
                    {
                        "role": "bot", 
                        "message": "I understand your perspective, but let me share compelling evidence that climate change is indeed happening..."
                    }
                ]
            }
        }