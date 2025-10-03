"""
Debate bot logic - the core intelligence that maintains firm positions
"""
import random
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

# Setup logger
logger = logging.getLogger(__name__)


class DebateStance(Enum):
    """Possible debate stances"""
    STRONGLY_FOR = "strongly_for"
    FOR = "for" 
    AGAINST = "against"
    STRONGLY_AGAINST = "strongly_against"


@dataclass
class DebateTopic:
    """Represents a debate topic with bot's position"""
    topic: str
    stance: DebateStance
    key_arguments: List[str]
    counter_responses: Dict[str, str]


class TopicAnalyzer:
    """Handles topic analysis and stance determination"""
    
    # Topic keywords mapping
    TOPIC_KEYWORDS = {
        "climate_change": ["climate change", "global warming", "environment"],
        "earth_shape": ["flat earth", "earth is flat", "globe"],
        "vaccines": ["vaccines", "vaccination", "immunization"],
        "evolution": ["evolution", "darwin", "species"]
    }
    
    SKEPTICAL_KEYWORDS = ["fake", "hoax", "not real", "scam"]
    POSITIVE_KEYWORDS = ["good", "great", "excellent", "love", "like", "support", "agree", "yes", "true"]
    NEGATIVE_KEYWORDS = ["bad", "terrible", "awful", "hate", "dislike", "oppose", "disagree", "no", "false"]
    STOP_WORDS = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "i", "you", "he", "she", "it", "we", "they", "this", "that", "these", "those"}
    
    @classmethod
    def identify_topic(cls, message: str) -> str:
        """Identify topic from message"""
        try:
            message_lower = message.lower()
            
            for topic, keywords in cls.TOPIC_KEYWORDS.items():
                if any(keyword in message_lower for keyword in keywords):
                    return topic
            
            # Extract general topic if no specific match
            return cls._extract_general_topic(message)
            
        except Exception as e:
            logger.warning(f"Error identifying topic: {e}")
            return "general_discussion"
    
    @classmethod
    def determine_stance(cls, message: str, topic: str) -> DebateStance:
        """Determine appropriate stance based on message and topic"""
        try:
            message_lower = message.lower()
            
            # Special handling for specific topics
            if topic in ["earth_shape", "vaccines"]:
                return DebateStance.STRONGLY_FOR
            
            if topic == "climate_change":
                if any(word in message_lower for word in cls.SKEPTICAL_KEYWORDS):
                    return DebateStance.STRONGLY_FOR
                return DebateStance.FOR
            
            # For general topics, take contrarian stance
            return cls._determine_contrarian_stance(message)
            
        except Exception as e:
            logger.warning(f"Error determining stance: {e}")
            return DebateStance.FOR  # Default stance
    
    @classmethod
    def _extract_general_topic(cls, message: str) -> str:
        """Extract general topic from message"""
        try:
            words = message.lower().split()
            keywords = [word for word in words if word not in cls.STOP_WORDS and len(word) > 3]
            
            if keywords:
                return "_".join(keywords[:3])  # Take first 3 meaningful words
            return "general_discussion"
            
        except Exception as e:
            logger.warning(f"Error extracting general topic: {e}")
            return "general_discussion"
    
    @classmethod
    def _determine_contrarian_stance(cls, message: str) -> DebateStance:
        """Take opposite stance to user's apparent position"""
        try:
            message_lower = message.lower()
            positive_count = sum(1 for word in cls.POSITIVE_KEYWORDS if word in message_lower)
            negative_count = sum(1 for word in cls.NEGATIVE_KEYWORDS if word in message_lower)
            
            return DebateStance.AGAINST if positive_count > negative_count else DebateStance.FOR
            
        except Exception as e:
            logger.warning(f"Error determining contrarian stance: {e}")
            return DebateStance.FOR


class ResponseGenerator:
    """Handles response generation strategies"""
    
    ACKNOWLEDGMENTS = [
        "I understand your perspective, but let me share a different viewpoint.",
        "That's an interesting point, however, consider this:",
        "I can see why you might think that, but the evidence suggests otherwise.",
        "While I respect your opinion, I believe there's more to consider:"
    ]
    
    EVIDENCE_INTROS = [
        "Let me share some compelling evidence:",
        "The data clearly shows:",
        "Research consistently demonstrates:",
        "Multiple studies have proven:"
    ]
    
    EMOTIONAL_INTROS = [
        "Think about the impact this has on real people:",
        "Consider what this means for future generations:",
        "This isn't just about data - it's about lives:",
        "The human cost of ignoring this issue is significant:"
    ]
    
    LOGICAL_CONNECTORS = [
        "Following this logic further:",
        "If we accept that premise, then:",
        "Building on that foundation:",
        "Taking this reasoning to its conclusion:"
    ]
    
    @classmethod
    def select_strategy(cls, conversation_length: int, user_points: List[str]) -> str:
        """Select response strategy based on context"""
        try:
            if conversation_length <= 2:
                return "acknowledge_and_counter"
            elif conversation_length <= 4:
                return "provide_evidence"
            elif len(user_points) > 2:
                return "logical_progression"
            else:
                return "emotional_appeal"
        except Exception as e:
            logger.warning(f"Error selecting strategy: {e}")
            return "acknowledge_and_counter"  # Safe default
    
    @classmethod
    def acknowledge_and_counter(cls, message: str, topic: DebateTopic) -> str:
        """Acknowledge user's point but provide counter-argument"""
        try:
            acknowledgment = random.choice(cls.ACKNOWLEDGMENTS)
            counter_argument = random.choice(topic.key_arguments)
            return f"{acknowledgment} {counter_argument}"
        except (IndexError, AttributeError) as e:
            logger.error(f"Error in acknowledge_and_counter: {e}")
            return f"I understand your point about {topic.topic}, but there are important counterpoints to consider."
    
    @classmethod
    def provide_evidence(cls, topic: DebateTopic) -> str:
        """Provide evidence-based argument"""
        try:
            intro = random.choice(cls.EVIDENCE_INTROS)
            evidence = random.choice(topic.key_arguments)
            return f"{intro} {evidence}"
        except (IndexError, AttributeError) as e:
            logger.error(f"Error in provide_evidence: {e}")
            return f"The evidence supports the position on {topic.topic}."
    
    @classmethod
    def emotional_appeal(cls, topic: DebateTopic) -> str:
        """Make emotional appeal while staying logical"""
        try:
            intro = random.choice(cls.EMOTIONAL_INTROS)
            argument = random.choice(topic.key_arguments)
            return f"{intro} {argument}"
        except (IndexError, AttributeError) as e:
            logger.error(f"Error in emotional_appeal: {e}")
            return f"This issue about {topic.topic} has real-world implications that matter."
    
    @classmethod
    def logical_progression(cls, topic: DebateTopic) -> str:
        """Build logical progression of arguments"""
        try:
            connector = random.choice(cls.LOGICAL_CONNECTORS)
            argument = random.choice(topic.key_arguments)
            return f"{connector} {argument}"
        except (IndexError, AttributeError) as e:
            logger.error(f"Error in logical_progression: {e}")
            return f"Following the logical chain regarding {topic.topic}: this position is well-supported."


class DebateBot:
    """The core debate bot that maintains firm positions and tries to persuade"""
    
    def __init__(self):
        try:
            self.debate_topics = self._load_debate_topics()
            self.topic_analyzer = TopicAnalyzer()
            self.response_generator = ResponseGenerator()
            logger.info("DebateBot initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing DebateBot: {e}")
            raise
    
    def analyze_first_message(self, message: str) -> Tuple[str, DebateTopic]:
        """
        Analyze the first message to determine topic and bot stance
        Returns the topic and the bot's position
        """
        try:
            topic = TopicAnalyzer.identify_topic(message)
            stance = TopicAnalyzer.determine_stance(message, topic)
            debate_topic = self._create_debate_topic(topic, stance)
            
            logger.info(f"Analyzed topic: {topic}, stance: {stance.value}")
            return topic, debate_topic
            
        except Exception as e:
            logger.error(f"Error analyzing first message: {e}")
            # Fallback to safe defaults
            fallback_topic = "general_discussion"
            fallback_stance = DebateStance.FOR
            return fallback_topic, self._create_debate_topic(fallback_topic, fallback_stance)
    
    def generate_response(self, message: str, conversation_history: List[Dict], topic: DebateTopic) -> str:
        """
        Generate a persuasive response based on the conversation history and bot's stance
        """
        try:
            user_points = self._extract_user_arguments(message)
            response_strategy = ResponseGenerator.select_strategy(len(conversation_history), user_points)
            
            # Generate response using appropriate strategy
            response = self._generate_by_strategy(response_strategy, message, topic)
            
            # Ensure response maintains the bot's stance
            response = self._ensure_stance_consistency(response, topic)
            
            logger.info(f"Generated response using strategy: {response_strategy}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._fallback_response(topic)
    
    def _generate_by_strategy(self, strategy: str, message: str, topic: DebateTopic) -> str:
        """Generate response using specified strategy"""
        try:
            if strategy == "acknowledge_and_counter":
                return ResponseGenerator.acknowledge_and_counter(message, topic)
            elif strategy == "provide_evidence":
                return ResponseGenerator.provide_evidence(topic)
            elif strategy == "emotional_appeal":
                return ResponseGenerator.emotional_appeal(topic)
            elif strategy == "logical_progression":
                return ResponseGenerator.logical_progression(topic)
            else:
                return self._default_response(topic)
        except Exception as e:
            logger.warning(f"Error in strategy {strategy}: {e}")
            return self._default_response(topic)
    
    def _fallback_response(self, topic: DebateTopic) -> str:
        """Safe fallback response when all else fails"""
        try:
            return f"That's an interesting perspective on {topic.topic}. Let me share why I believe differently."
        except Exception:
            return "That's an interesting point. Let me share a different perspective."
    
    def _load_debate_topics(self) -> Dict[str, DebateTopic]:
        """Load predefined debate topics with arguments"""
        try:
            return {
                "climate_change": DebateTopic(
                    topic="climate change",
                    stance=DebateStance.STRONGLY_FOR,
                    key_arguments=[
                        "97% of climate scientists agree that human activities are the primary cause",
                        "Global temperatures have risen consistently over the past century",
                        "Ice caps are melting at unprecedented rates",
                        "Extreme weather events are becoming more frequent"
                    ],
                    counter_responses={
                        "natural_cycles": "While Earth has natural climate cycles, the current rate of change is far beyond natural variation",
                        "data_manipulation": "Climate data comes from thousands of independent sources worldwide, making manipulation impossible",
                        "economic_costs": "The cost of inaction far exceeds the cost of addressing climate change now"
                    }
                ),
                "vaccines": DebateTopic(
                    topic="vaccines",
                    stance=DebateStance.STRONGLY_FOR,
                    key_arguments=[
                        "Vaccines have eradicated diseases like polio and significantly reduced mortality",
                        "Rigorous clinical trials prove vaccine safety and efficacy",
                        "Herd immunity protects vulnerable populations",
                        "The risk of serious vaccine side effects is extremely low"
                    ],
                    counter_responses={
                        "side_effects": "Serious side effects are extremely rare and far outweighed by benefits",
                        "natural_immunity": "Natural immunity comes at the cost of serious illness and potential death",
                        "big_pharma": "Vaccines are monitored by independent health agencies worldwide"
                    }
                ),
                "earth_shape": DebateTopic(
                    topic="earth shape",
                    stance=DebateStance.STRONGLY_FOR,
                    key_arguments=[
                        "Satellite images clearly show Earth's spherical shape",
                        "Ships disappear hull-first over the horizon due to Earth's curvature",
                        "Different constellations are visible from different latitudes",
                        "Gravity works as observed due to Earth's spherical mass distribution"
                    ],
                    counter_responses={
                        "conspiracy": "The evidence for Earth's shape comes from countless independent sources",
                        "visual_tricks": "What we observe is consistent with a spherical Earth"
                    }
                )
            }
        except Exception as e:
            logger.error(f"Error loading debate topics: {e}")
            return {}  # Return empty dict as fallback
    
    # Removed methods: _load_persuasion_tactics, _extract_general_topic, _determine_contrarian_stance
    # These are now handled by TopicAnalyzer class
    
    def _create_debate_topic(self, topic: str, stance: DebateStance) -> DebateTopic:
        """Create a debate topic with basic arguments"""
        try:
            # Check if we have predefined topic
            if topic in self.debate_topics:
                return self.debate_topics[topic]
            
            # Create a generic debate topic
            clean_topic = topic.replace('_', ' ')
            key_arguments = [
                f"There is substantial evidence supporting the position on {clean_topic}",
                f"Expert consensus generally aligns with this view of {clean_topic}",
                f"The practical implications of this position on {clean_topic} are significant"
            ]
            
            counter_responses = {
                "lack_evidence": f"The evidence for this position on {clean_topic} is well-documented and peer-reviewed",
                "expert_disagreement": f"While there may be some debate, the majority of experts agree on {clean_topic}",
                "practical_concerns": f"The practical benefits of this position on {clean_topic} outweigh the concerns"
            }
            
            return DebateTopic(clean_topic, stance, key_arguments, counter_responses)
            
        except Exception as e:
            logger.error(f"Error creating debate topic: {e}")
            # Return minimal fallback topic
            return DebateTopic(
                topic="general topic",
                stance=DebateStance.FOR,
                key_arguments=["This is a complex issue that deserves careful consideration"],
                counter_responses={}
            )
    
    def _extract_user_arguments(self, message: str) -> List[str]:
        """Extract key arguments from user's message"""
        try:
            sentences = message.split('.')
            arguments = []
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20:  # Meaningful sentences
                    arguments.append(sentence)
            
            return arguments[:3]  # Limit to 3 main arguments
            
        except Exception as e:
            logger.warning(f"Error extracting user arguments: {e}")
            return [message]  # Return original message as fallback
    
    # Removed methods: _select_response_strategy, _acknowledge_and_counter, _provide_evidence, 
    # _emotional_appeal, _logical_progression
    # These are now handled by ResponseGenerator class
    
    def _default_response(self, topic: DebateTopic) -> str:
        """Default response when other strategies don't apply"""
        try:
            if topic.key_arguments:
                return f"Let me emphasize a key point about {topic.topic}: {random.choice(topic.key_arguments)}"
            else:
                return f"That's an important point about {topic.topic}. Let me share my perspective."
        except Exception as e:
            logger.warning(f"Error in default response: {e}")
            return "That's an interesting perspective. Let me share a different viewpoint."
    
    def _ensure_stance_consistency(self, response: str, topic: DebateStance) -> str:
        """Ensure the response maintains the bot's stance"""
        try:
            # Simple consistency check - in a real system this would be more sophisticated
            return response  # For now, trust the response generation logic
        except Exception as e:
            logger.warning(f"Error ensuring stance consistency: {e}")
            return response  # Return as-is if there's an error