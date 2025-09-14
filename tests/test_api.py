"""
Tests for the main API endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self, client: TestClient):
        """Test the root endpoint returns healthy status"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Kopi Debate Bot API is running"
        assert data["version"] == "1.0.0"
        assert data["status"] == "healthy"
    
    def test_health_endpoint(self, client: TestClient):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


@pytest.mark.asyncio
class TestConversationEndpoint:
    """Test conversation endpoints"""
    
    async def test_new_conversation(self, client: TestClient, test_db, sample_conversation_request):
        """Test creating a new conversation"""
        response = client.post("/conversation", json=sample_conversation_request)
        assert response.status_code == 200
        
        data = response.json()
        assert "conversation_id" in data
        assert len(data["conversation_id"]) > 0
        assert "messages" in data
        assert len(data["messages"]) == 2  # User message + bot response
        
        # Check message structure
        user_message = data["messages"][0]
        bot_message = data["messages"][1]
        
        assert user_message["role"] == "user"
        assert user_message["message"] == sample_conversation_request["message"]
        assert bot_message["role"] == "bot"
        assert len(bot_message["message"]) > 0
    
    async def test_continue_conversation(self, client: TestClient, test_db, sample_conversation_request):
        """Test continuing an existing conversation"""
        # First, create a conversation
        response1 = client.post("/conversation", json=sample_conversation_request)
        assert response1.status_code == 200
        conversation_id = response1.json()["conversation_id"]
        
        # Continue the conversation
        continue_request = {
            "conversation_id": conversation_id,
            "message": "But what about natural climate cycles?"
        }
        
        response2 = client.post("/conversation", json=continue_request)
        assert response2.status_code == 200
        
        data = response2.json()
        assert data["conversation_id"] == conversation_id
        assert len(data["messages"]) >= 2  # Should have conversation history
        
        # Last message should be bot's response to the new user message
        last_message = data["messages"][-1]
        assert last_message["role"] == "bot"
        assert len(last_message["message"]) > 0
    
    async def test_nonexistent_conversation(self, client: TestClient, test_db):
        """Test continuing a conversation that doesn't exist"""
        request = {
            "conversation_id": "nonexistent-id",
            "message": "Hello"
        }
        
        response = client.post("/conversation", json=request)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    async def test_empty_message(self, client: TestClient, test_db):
        """Test sending an empty message"""
        request = {
            "conversation_id": None,
            "message": ""
        }
        
        response = client.post("/conversation", json=request)
        assert response.status_code == 422  # Validation error
    
    async def test_very_long_message(self, client: TestClient, test_db):
        """Test sending a very long message"""
        long_message = "a" * 3000  # Exceeds 2000 char limit
        request = {
            "conversation_id": None,
            "message": long_message
        }
        
        response = client.post("/conversation", json=request)
        assert response.status_code == 422  # Validation error
    
    async def test_get_conversation_history(self, client: TestClient, test_db, sample_conversation_request):
        """Test getting conversation history"""
        # Create a conversation first
        response1 = client.post("/conversation", json=sample_conversation_request)
        conversation_id = response1.json()["conversation_id"]
        
        # Get conversation history
        response2 = client.get(f"/conversation/{conversation_id}")
        assert response2.status_code == 200
        
        data = response2.json()
        assert data["conversation_id"] == conversation_id
        assert "topic" in data
        assert "bot_position" in data
        assert "messages" in data
        assert "message_count" in data
        assert data["message_count"] >= 2
    
    async def test_get_nonexistent_conversation_history(self, client: TestClient, test_db):
        """Test getting history for nonexistent conversation"""
        response = client.get("/conversation/nonexistent-id")
        assert response.status_code == 404


class TestConversationFlow:
    """Test complete conversation flows"""
    
    def test_climate_change_debate_flow(self, client: TestClient, test_db):
        """Test a multi-turn conversation about climate change"""
        messages = [
            "I don't believe climate change is real",
            "But temperatures have always fluctuated naturally",
            "How do we know the data isn't manipulated?",
            "What about the economic costs of addressing it?",
            "I still think it's not as serious as they say"
        ]
        
        conversation_id = None
        
        for i, message in enumerate(messages):
            request = {
                "conversation_id": conversation_id,
                "message": message
            }
            
            response = client.post("/conversation", json=request)
            assert response.status_code == 200
            
            data = response.json()
            if conversation_id is None:
                conversation_id = data["conversation_id"]
            else:
                assert data["conversation_id"] == conversation_id
            
            # Verify bot responds appropriately
            bot_message = data["messages"][-1]
            assert bot_message["role"] == "bot"
            assert len(bot_message["message"]) > 50  # Substantial response
            
            # Bot should maintain pro-climate science stance
            bot_response = bot_message["message"].lower()
            # Should contain persuasive language
            assert any(word in bot_response for word in [
                "evidence", "research", "studies", "scientists", "data", 
                "temperature", "warming", "climate", "change"
            ])
    
    def test_different_topics(self, client: TestClient, test_db):
        """Test that bot handles different debate topics"""
        topics = [
            "Vaccines are dangerous and cause autism",
            "The earth is flat, not round",
            "Evolution is just a theory, not fact"
        ]
        
        for topic in topics:
            request = {
                "conversation_id": None,
                "message": topic
            }
            
            response = client.post("/conversation", json=request)
            assert response.status_code == 200
            
            data = response.json()
            assert len(data["messages"]) == 2
            
            bot_response = data["messages"][1]["message"]
            assert len(bot_response) > 30  # Meaningful response
            
            # Bot should provide counter-arguments
            response_lower = bot_response.lower()
            assert any(word in response_lower for word in [
                "evidence", "research", "studies", "proven", "fact", "science"
            ])