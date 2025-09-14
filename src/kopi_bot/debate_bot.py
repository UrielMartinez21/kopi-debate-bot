"""
Debate bot logic - the core intelligence that maintains firm positions
"""
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


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


class DebateBot:
    """The core debate bot that maintains firm positions and tries to persuade"""
    
    def __init__(self):
        self.debate_topics = self._load_debate_topics()
        self.persuasion_tactics = self._load_persuasion_tactics()
    
    def analyze_first_message(self, message: str) -> Tuple[str, DebateTopic]:
        """
        Analyze the first message to determine topic and bot stance
        Returns the topic and the bot's position
        """
        message_lower = message.lower()
        
        # Look for keywords to determine topic and stance
        if any(word in message_lower for word in ["climate change", "global warming", "environment"]):
            topic = "climate change"
            # If user seems skeptical, bot takes strong pro-climate science stance
            if any(word in message_lower for word in ["fake", "hoax", "not real", "scam"]):
                stance = DebateStance.STRONGLY_FOR
            else:
                stance = DebateStance.FOR
                
        elif any(word in message_lower for word in ["flat earth", "earth is flat", "globe"]):
            topic = "earth shape"
            # Bot always argues for round earth
            stance = DebateStance.STRONGLY_FOR
            
        elif any(word in message_lower for word in ["vaccines", "vaccination", "immunization"]):
            topic = "vaccines"
            # Bot always pro-vaccine
            stance = DebateStance.STRONGLY_FOR
            
        elif any(word in message_lower for word in ["evolution", "darwin", "species"]):
            topic = "evolution"
            stance = DebateStance.FOR
            
        else:
            # Default: extract general topic and take a contrarian stance
            topic = self._extract_general_topic(message)
            stance = self._determine_contrarian_stance(message)
        
        debate_topic = self._create_debate_topic(topic, stance)
        return topic, debate_topic
    
    def generate_response(self, message: str, conversation_history: List[Dict], topic: DebateTopic) -> str:
        """
        Generate a persuasive response based on the conversation history and bot's stance
        """
        # Analyze user's message for counter-arguments
        user_points = self._extract_user_arguments(message)
        
        # Select appropriate response strategy
        response_strategy = self._select_response_strategy(len(conversation_history), user_points)
        
        # Generate response based on strategy
        if response_strategy == "acknowledge_and_counter":
            response = self._acknowledge_and_counter(message, topic, user_points)
        elif response_strategy == "provide_evidence":
            response = self._provide_evidence(topic)
        elif response_strategy == "emotional_appeal":
            response = self._emotional_appeal(topic)
        elif response_strategy == "logical_progression":
            response = self._logical_progression(topic, user_points)
        else:
            response = self._default_response(topic)
        
        # Ensure response maintains the bot's stance
        response = self._ensure_stance_consistency(response, topic)
        
        return response
    
    def _load_debate_topics(self) -> Dict[str, DebateTopic]:
        """Load predefined debate topics with arguments"""
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
            )
        }
    
    def _load_persuasion_tactics(self) -> List[str]:
        """Load persuasion tactics for more effective arguments"""
        return [
            "use_credible_sources",
            "acknowledge_valid_concerns", 
            "provide_specific_examples",
            "appeal_to_shared_values",
            "use_logical_progression",
            "create_emotional_connection"
        ]
    
    def _extract_general_topic(self, message: str) -> str:
        """Extract a general topic from the message"""
        # Simple topic extraction - in production would use NLP
        words = message.lower().split()
        # Remove common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "i", "you", "he", "she", "it", "we", "they", "this", "that", "these", "those"}
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        if keywords:
            return " ".join(keywords[:3])  # Take first 3 meaningful words
        return "general discussion"
    
    def _determine_contrarian_stance(self, message: str) -> DebateStance:
        """Determine a contrarian stance based on user's apparent position"""
        # Simple sentiment analysis - take opposite stance
        positive_words = ["good", "great", "excellent", "love", "like", "support", "agree", "yes", "true"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "oppose", "disagree", "no", "false"]
        
        message_lower = message.lower()
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return DebateStance.AGAINST
        else:
            return DebateStance.FOR
    
    def _create_debate_topic(self, topic: str, stance: DebateStance) -> DebateTopic:
        """Create a debate topic with basic arguments"""
        if topic in self.debate_topics:
            return self.debate_topics[topic]
        
        # Create a generic debate topic
        key_arguments = [
            f"There is substantial evidence supporting the position on {topic}",
            f"Expert consensus generally aligns with this view of {topic}",
            f"The practical implications of this position on {topic} are significant"
        ]
        
        counter_responses = {
            "lack_evidence": f"The evidence for this position on {topic} is well-documented and peer-reviewed",
            "expert_disagreement": f"While there may be some debate, the majority of experts agree on {topic}",
            "practical_concerns": f"The practical benefits of this position on {topic} outweigh the concerns"
        }
        
        return DebateTopic(topic, stance, key_arguments, counter_responses)
    
    def _extract_user_arguments(self, message: str) -> List[str]:
        """Extract key arguments from user's message"""
        # Simple argument extraction
        sentences = message.split('.')
        arguments = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Meaningful sentences
                arguments.append(sentence)
        
        return arguments[:3]  # Limit to 3 main arguments
    
    def _select_response_strategy(self, conversation_length: int, user_points: List[str]) -> str:
        """Select the best response strategy based on context"""
        if conversation_length <= 2:
            return "acknowledge_and_counter"
        elif conversation_length <= 4:
            return "provide_evidence"
        elif len(user_points) > 2:
            return "logical_progression"
        else:
            return "emotional_appeal"
    
    def _acknowledge_and_counter(self, message: str, topic: DebateTopic, user_points: List[str]) -> str:
        """Acknowledge user's point but provide counter-argument"""
        acknowledgments = [
            "I understand your perspective, but let me share a different viewpoint.",
            "That's an interesting point, however, consider this:",
            "I can see why you might think that, but the evidence suggests otherwise.",
            "While I respect your opinion, I believe there's more to consider:"
        ]
        
        acknowledgment = random.choice(acknowledgments)
        counter_argument = random.choice(topic.key_arguments)
        
        return f"{acknowledgment} {counter_argument}"
    
    def _provide_evidence(self, topic: DebateTopic) -> str:
        """Provide evidence-based argument"""
        evidence_intro = [
            "Let me share some compelling evidence:",
            "The data clearly shows:",
            "Research consistently demonstrates:",
            "Multiple studies have proven:"
        ]
        
        intro = random.choice(evidence_intro)
        evidence = random.choice(topic.key_arguments)
        
        return f"{intro} {evidence}"
    
    def _emotional_appeal(self, topic: DebateTopic) -> str:
        """Make an emotional appeal while staying logical"""
        emotional_intros = [
            "Think about the impact this has on real people:",
            "Consider what this means for future generations:",
            "This isn't just about data - it's about lives:",
            "The human cost of ignoring this issue is significant:"
        ]
        
        intro = random.choice(emotional_intros)
        argument = random.choice(topic.key_arguments)
        
        return f"{intro} {argument}"
    
    def _logical_progression(self, topic: DebateTopic, user_points: List[str]) -> str:
        """Build a logical progression of arguments"""
        logical_connectors = [
            "Following this logic further:",
            "If we accept that premise, then:",
            "Building on that foundation:",
            "Taking this reasoning to its conclusion:"
        ]
        
        connector = random.choice(logical_connectors)
        argument = random.choice(topic.key_arguments)
        
        return f"{connector} {argument}"
    
    def _default_response(self, topic: DebateTopic) -> str:
        """Default response when other strategies don't apply"""
        return f"Let me emphasize a key point about {topic.topic}: {random.choice(topic.key_arguments)}"
    
    def _ensure_stance_consistency(self, response: str, topic: DebateTopic) -> str:
        """Ensure the response maintains the bot's stance"""
        # Add stance reinforcement if needed
        if topic.stance in [DebateStance.STRONGLY_FOR, DebateStance.FOR]:
            if "however" in response.lower() or "but" in response.lower():
                return response
            # Already maintains positive stance
        
        return response