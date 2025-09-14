"""
Simplified tests that work without complex fixtures
"""
import pytest
from fastapi.testclient import TestClient
import tempfile
import os

# Create a simple test client without database dependencies
def test_health_endpoints():
    """Test health endpoints work"""
    from kopi_bot.main import app
    client = TestClient(app)
    
    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    
    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_debate_bot_basic():
    """Test basic debate bot functionality"""
    from kopi_bot.debate_bot import DebateBot, DebateStance
    
    bot = DebateBot()
    
    # Test initialization
    assert bot.debate_topics is not None
    assert bot.persuasion_tactics is not None
    
    # Test message analysis
    topic, debate_topic = bot.analyze_first_message("Climate change is fake")
    assert "climate" in topic.lower()
    assert debate_topic.stance == DebateStance.STRONGLY_FOR
    
    # Test response generation
    response = bot.generate_response("Test message", [], debate_topic)
    assert len(response) > 0
    assert isinstance(response, str)


def test_schemas():
    """Test Pydantic schemas work correctly"""
    from kopi_bot.schemas import ConversationRequest, ConversationResponse, MessageData, MessageRole
    
    # Test request schema
    request = ConversationRequest(
        conversation_id=None,
        message="Test message"
    )
    assert request.conversation_id is None
    assert request.message == "Test message"
    
    # Test response schema
    messages = [
        MessageData(role=MessageRole.USER, message="User message"),
        MessageData(role=MessageRole.BOT, message="Bot response")
    ]
    response = ConversationResponse(
        conversation_id="test-id",
        messages=messages
    )
    assert response.conversation_id == "test-id"
    assert len(response.messages) == 2


def test_config():
    """Test configuration loading"""
    from kopi_bot.config import Settings
    
    settings = Settings()
    assert settings.app_name == "Kopi Debate Bot"
    assert settings.max_conversation_history == 5
    assert settings.max_message_length == 2000
    assert settings.response_timeout == 30


def test_debate_topics():
    """Test debate topic handling"""
    from kopi_bot.debate_bot import DebateBot, DebateStance
    
    bot = DebateBot()
    
    # Test different topic recognition
    test_cases = [
        ("Climate change is fake", "climate"),
        ("Vaccines are dangerous", "vaccine"),
        ("The earth is flat", "earth"),
        ("Evolution is wrong", "evolution")
    ]
    
    for message, expected_topic in test_cases:
        topic, debate_topic = bot.analyze_first_message(message)
        assert expected_topic in topic.lower()
        assert debate_topic.stance in [DebateStance.FOR, DebateStance.STRONGLY_FOR]


def test_persuasion_responses():
    """Test that bot generates persuasive responses"""
    from kopi_bot.debate_bot import DebateBot, DebateTopic, DebateStance
    
    bot = DebateBot()
    
    # Create a test topic
    topic = DebateTopic(
        topic="test topic",
        stance=DebateStance.STRONGLY_FOR,
        key_arguments=["Strong evidence supports this position"],
        counter_responses={"objection": "Here's why that's wrong"}
    )
    
    # Test different response strategies
    responses = []
    for i in range(3):
        response = bot.generate_response(f"Test argument {i}", [], topic)
        responses.append(response)
        assert len(response) > 20  # Substantial responses
    
    # Responses should be different
    assert len(set(responses)) > 1  # At least some variety


if __name__ == "__main__":
    # Run basic tests
    test_health_endpoints()
    test_debate_bot_basic()
    test_schemas()
    test_config()
    test_debate_topics()
    test_persuasion_responses()
    print("All basic tests passed!")