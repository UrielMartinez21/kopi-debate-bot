"""
Tests for the debate bot logic
"""
import pytest
from kopi_bot.debate_bot import DebateBot, DebateStance, DebateTopic


class TestDebateBot:
    """Test the debate bot logic"""
    
    def test_bot_initialization(self):
        """Test that bot initializes correctly"""
        bot = DebateBot()
        assert bot.debate_topics is not None
        assert bot.persuasion_tactics is not None
        assert len(bot.debate_topics) > 0
        assert len(bot.persuasion_tactics) > 0
    
    def test_analyze_climate_change_message(self):
        """Test analyzing climate change related messages"""
        bot = DebateBot()
        
        # Test skeptical message
        topic, debate_topic = bot.analyze_first_message("Climate change is a hoax")
        assert "climate" in topic.lower()
        assert debate_topic.stance == DebateStance.STRONGLY_FOR
        
        # Test neutral message
        topic, debate_topic = bot.analyze_first_message("Tell me about climate change")
        assert "climate" in topic.lower()
        assert debate_topic.stance == DebateStance.FOR
    
    def test_analyze_vaccines_message(self):
        """Test analyzing vaccine related messages"""
        bot = DebateBot()
        
        topic, debate_topic = bot.analyze_first_message("Vaccines cause autism")
        assert "vaccine" in topic.lower()
        assert debate_topic.stance == DebateStance.STRONGLY_FOR
    
    def test_analyze_flat_earth_message(self):
        """Test analyzing flat earth messages"""
        bot = DebateBot()
        
        topic, debate_topic = bot.analyze_first_message("The earth is flat")
        assert "earth" in topic.lower()
        assert debate_topic.stance == DebateStance.STRONGLY_FOR
    
    def test_analyze_general_message(self):
        """Test analyzing general messages"""
        bot = DebateBot()
        
        topic, debate_topic = bot.analyze_first_message("I love chocolate ice cream")
        assert len(topic) > 0
        assert debate_topic.stance in [DebateStance.FOR, DebateStance.AGAINST]
    
    def test_generate_response_new_conversation(self):
        """Test generating response for new conversation"""
        bot = DebateBot()
        
        # Create a debate topic
        topic = DebateTopic(
            topic="climate change",
            stance=DebateStance.STRONGLY_FOR,
            key_arguments=["Evidence shows climate change is real"],
            counter_responses={"skepticism": "Multiple studies confirm the reality"}
        )
        
        response = bot.generate_response("Climate change is fake", [], topic)
        assert len(response) > 0
        assert isinstance(response, str)
    
    def test_generate_response_ongoing_conversation(self):
        """Test generating response for ongoing conversation"""
        bot = DebateBot()
        
        conversation_history = [
            {"role": "user", "message": "Climate change is fake"},
            {"role": "bot", "message": "Evidence shows it's real"}
        ]
        
        topic = DebateTopic(
            topic="climate change",
            stance=DebateStance.STRONGLY_FOR,
            key_arguments=["Temperature data confirms warming"],
            counter_responses={"natural_cycles": "Current rate exceeds natural variation"}
        )
        
        response = bot.generate_response("What about natural cycles?", conversation_history, topic)
        assert len(response) > 0
        assert isinstance(response, str)
    
    def test_extract_user_arguments(self):
        """Test extracting arguments from user messages"""
        bot = DebateBot()
        
        message = "I think climate change is fake. The data is manipulated. Scientists are lying for money."
        arguments = bot._extract_user_arguments(message)
        
        assert isinstance(arguments, list)
        assert len(arguments) <= 3
        for arg in arguments:
            assert len(arg) > 20  # Meaningful arguments
    
    def test_response_strategies(self):
        """Test different response strategies"""
        bot = DebateBot()
        
        topic = DebateTopic(
            topic="test topic",
            stance=DebateStance.FOR,
            key_arguments=["Test argument"],
            counter_responses={"test": "Test response"}
        )
        
        # Test different conversation lengths
        strategies = []
        for length in [1, 3, 5]:
            strategy = bot._select_response_strategy(length, ["test argument"])
            strategies.append(strategy)
        
        # Should return valid strategies
        valid_strategies = ["acknowledge_and_counter", "provide_evidence", "emotional_appeal", "logical_progression"]
        for strategy in strategies:
            assert strategy in valid_strategies


class TestDebateTopic:
    """Test debate topic functionality"""
    
    def test_debate_topic_creation(self):
        """Test creating a debate topic"""
        topic = DebateTopic(
            topic="test topic",
            stance=DebateStance.FOR,
            key_arguments=["argument 1", "argument 2"],
            counter_responses={"objection": "response"}
        )
        
        assert topic.topic == "test topic"
        assert topic.stance == DebateStance.FOR
        assert len(topic.key_arguments) == 2
        assert "objection" in topic.counter_responses
    
    def test_debate_stance_enum(self):
        """Test debate stance enumeration"""
        assert DebateStance.STRONGLY_FOR.value == "strongly_for"
        assert DebateStance.FOR.value == "for"
        assert DebateStance.AGAINST.value == "against"
        assert DebateStance.STRONGLY_AGAINST.value == "strongly_against"


class TestPersuasionTactics:
    """Test persuasion tactics"""
    
    def test_persuasion_methods(self):
        """Test different persuasion methods"""
        bot = DebateBot()
        
        topic = DebateTopic(
            topic="climate change",
            stance=DebateStance.STRONGLY_FOR,
            key_arguments=["Scientific consensus supports climate change"],
            counter_responses={}
        )
        
        # Test acknowledge and counter
        response = bot._acknowledge_and_counter("Climate change is fake", topic, ["fake"])
        assert len(response) > 0
        assert any(word in response.lower() for word in ["understand", "perspective", "however", "but"])
        
        # Test provide evidence
        response = bot._provide_evidence(topic)
        assert len(response) > 0
        assert any(word in response.lower() for word in ["evidence", "data", "research", "studies"])
        
        # Test emotional appeal
        response = bot._emotional_appeal(topic)
        assert len(response) > 0
        assert any(word in response.lower() for word in ["people", "impact", "lives", "future"])
        
        # Test logical progression
        response = bot._logical_progression(topic, ["some point"])
        assert len(response) > 0
        assert any(word in response.lower() for word in ["logic", "reasoning", "conclusion", "premise"])


class TestResponseConsistency:
    """Test that bot maintains consistent positions"""
    
    def test_stance_consistency(self):
        """Test that bot maintains its stance throughout conversation"""
        bot = DebateBot()
        
        # Test climate change stance consistency
        topic, debate_topic = bot.analyze_first_message("Climate change is fake")
        
        # Generate multiple responses
        responses = []
        for i in range(5):
            response = bot.generate_response(f"Climate point {i}", [], debate_topic)
            responses.append(response.lower())
        
        # All responses should support climate science (pro-climate stance)
        for response in responses:
            # Should not contain language that supports climate denial
            assert not any(word in response for word in ["hoax", "fake", "conspiracy", "lie"])
            # Should contain pro-science language
            assert any(word in response for word in ["evidence", "science", "research", "data", "studies"])