"""
Feedback Engine - Phase 2 core

Coordinates reviewers, memory, entity tracking, and AI providers
to generate authentic scene-by-scene feedback
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

# Add backend to path
backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from models.screenplay import Screenplay, Scene
from models.reviewer import ReviewerProfile, ReviewerState, EmotionalState, REVIEWER_PROFILES
from models.memory import MemoryManager, SceneDigest
from models.entity import EntityTracker
from models.question import Question, QuestionTracker, QuestionStatus, NarrativeWeight
from services.ai_provider import AIProvider, AIMessage, AIProviderFactory
from services.compressor import SceneCompressor


class SceneFeedback(BaseModel):
    """Feedback for a single scene from one reviewer"""
    scene_number: int
    reviewer_id: str
    reviewer_name: str

    # The actual feedback text
    feedback: str

    # Emotional state after this scene
    emotional_state: EmotionalState

    # Questions raised or answered
    questions_raised: List[str] = Field(default_factory=list)
    questions_answered: List[str] = Field(default_factory=list)

    # Character impressions updated
    character_impressions: Dict[str, str] = Field(default_factory=dict)

    # Overall ratings
    scene_rating: Optional[float] = None  # 0-10 rating for this scene


class ReviewSession(BaseModel):
    """A complete review session for a screenplay"""
    screenplay_title: str
    total_scenes: int
    reviewers: List[str]  # Reviewer IDs

    # All feedback generated
    all_feedback: List[SceneFeedback] = Field(default_factory=list)

    # Final summary
    final_summary: Optional[str] = None

    # Metadata
    ai_provider: str
    model_used: str
    total_cost: float = 0.0


class FeedbackEngine:
    """
    Main engine for generating screenplay feedback

    Coordinates:
    - Multiple AI reviewers with different personalities
    - Memory management (sliding window)
    - Entity tracking (character importance)
    - Question tracking (mysteries/open questions)
    - Emotional continuity (100% preserved)
    """

    def __init__(
        self,
        ai_providers: Dict[str, AIProvider],
        reviewer_configs: Optional[List[Dict]] = None
    ):
        """
        Initialize feedback engine

        Args:
            ai_providers: Dict of provider_name -> AIProvider instance
                         e.g., {"anthropic": AnthropicProvider(), "openai": OpenAIProvider()}
            reviewer_configs: List of reviewer configs with format:
                             [{"profile": "blockbuster_fan", "ai_provider": "anthropic"},
                              {"profile": "blockbuster_fan", "ai_provider": "openai"}, ...]
                             If None, uses all profiles with first available provider
        """
        self.ai_providers = ai_providers

        # Initialize reviewers
        if reviewer_configs is None:
            # Default: use all profiles with first available provider
            first_provider = list(ai_providers.keys())[0]
            reviewer_configs = [
                {"profile": profile_id, "ai_provider": first_provider}
                for profile_id in REVIEWER_PROFILES.keys()
            ]

        self.reviewers: Dict[str, ReviewerState] = {}
        for config in reviewer_configs:
            profile_id = config["profile"]
            provider_name = config["ai_provider"]

            if profile_id not in REVIEWER_PROFILES:
                raise ValueError(f"Unknown reviewer profile: {profile_id}")
            if provider_name not in ai_providers:
                raise ValueError(f"Unknown AI provider: {provider_name}")

            profile = REVIEWER_PROFILES[profile_id]

            # Create unique reviewer ID combining profile and AI
            reviewer_id = f"{profile_id}_{provider_name}"

            self.reviewers[reviewer_id] = ReviewerState(
                reviewer_id=reviewer_id,
                profile=profile,
                ai_provider_name=provider_name
            )

        # Initialize supporting systems (shared across reviewers)
        self.memory = MemoryManager()
        self.entity_tracker: Optional[EntityTracker] = None
        self.question_tracker = QuestionTracker()
        self.compressor: Optional[SceneCompressor] = None

    def review_screenplay(
        self,
        screenplay: Screenplay,
        entity_tracker: EntityTracker
    ) -> ReviewSession:
        """
        Review an entire screenplay scene-by-scene

        Args:
            screenplay: Parsed screenplay
            entity_tracker: Pre-populated entity tracker

        Returns:
            ReviewSession with all feedback
        """
        self.entity_tracker = entity_tracker
        self.compressor = SceneCompressor(entity_tracker=entity_tracker)

        # Create review session
        provider_names = list(self.ai_providers.keys())
        session = ReviewSession(
            screenplay_title=screenplay.title or "Untitled",
            total_scenes=screenplay.total_scenes,
            reviewers=list(self.reviewers.keys()),
            ai_provider=", ".join(provider_names),
            model_used="Mixed" if len(self.ai_providers) > 1 else list(self.ai_providers.values())[0].get_model_name()
        )

        print(f"\n{'='*60}")
        print(f"REVIEWING: {session.screenplay_title}")
        print(f"Reviewers: {len(self.reviewers)} total")
        for reviewer_id, reviewer in self.reviewers.items():
            ai_brain = reviewer.ai_provider_name.upper()
            print(f"  - {reviewer.profile.name} ({ai_brain} brain)")
        print(f"{'='*60}\n")

        # Process each scene
        for scene in screenplay.scenes:
            print(f"\n--- SCENE {scene.scene_number}: {scene.heading} ---")

            # Review scene with each reviewer
            for reviewer_id, reviewer_state in self.reviewers.items():
                feedback = self._review_scene(
                    scene=scene,
                    reviewer_state=reviewer_state,
                    screenplay=screenplay
                )

                session.all_feedback.append(feedback)
                session.total_cost += 0.0  # Will be updated when we track costs

                print(f"\n{reviewer_state.profile.name}:")
                print(f"  {feedback.feedback[:150]}...")
                print(f"  Engagement: {feedback.emotional_state.engagement_level:.2f}")
                print(f"  Enjoyment: {feedback.emotional_state.enjoyment:.2f}")

            # Update memory system
            self._update_memory(scene)

        print(f"\n{'='*60}")
        print("REVIEW COMPLETE")
        print(f"{'='*60}\n")

        return session

    def _review_scene(
        self,
        scene: Scene,
        reviewer_state: ReviewerState,
        screenplay: Screenplay
    ) -> SceneFeedback:
        """
        Generate feedback for a single scene from one reviewer

        This is where the magic happens - constructing context and prompting AI
        """
        # Build context for this reviewer
        context = self._build_reviewer_context(scene, reviewer_state)

        # Build prompt
        prompt = self._build_scene_prompt(scene, reviewer_state, context)

        # Get AI response from this reviewer's assigned provider
        provider = self.ai_providers[reviewer_state.ai_provider_name]

        messages = [
            AIMessage(role="system", content=reviewer_state.profile.system_prompt),
            AIMessage(role="user", content=prompt)
        ]

        response = provider.chat(messages, temperature=0.8, max_tokens=800)

        # Parse response into structured feedback
        feedback = self._parse_feedback_response(
            response.content,
            scene,
            reviewer_state
        )

        # Update reviewer state
        reviewer_state.add_emotional_state(feedback.emotional_state)
        reviewer_state.current_scene = scene.scene_number
        reviewer_state.scenes_reviewed += 1

        # Update character opinions
        for char_name, opinion in feedback.character_impressions.items():
            reviewer_state.character_opinions[char_name] = opinion

        # Update question tracker
        for question in feedback.questions_raised:
            self.question_tracker.add_question(
                question=question,
                scene_number=scene.scene_number,
                reviewer_id=reviewer_state.reviewer_id
            )

        for question_id in feedback.questions_answered:
            self.question_tracker.mark_answered(question_id, scene.scene_number)

        return feedback

    def _build_reviewer_context(self, scene: Scene, reviewer_state: ReviewerState) -> Dict:
        """
        Build context for reviewer at this moment

        Includes:
        - Recent scenes (full detail)
        - Historical scene digests (compressed plot, full emotions)
        - High-importance entities (never forgotten)
        - Important open questions
        - Reviewer's own emotional journey
        """
        context = {}

        # Recent memory
        context['recent_scenes'] = self.memory.recent_memory.scenes

        # Historical summaries
        context['earlier_summaries'] = [
            f"Scene {d.scene_number}: {d.summary}"
            for d in self.memory.historical_memory.digests[-5:]  # Last 5 digests
        ]

        # High-importance entities
        high_importance = self.entity_tracker.get_high_importance_entities()
        context['key_characters'] = [
            {
                'name': e.name,
                'importance': e.importance_score,
                'appears_in': e.total_appearances,
                'role': e.narrative_function
            }
            for e in high_importance[:5]  # Top 5
        ]

        # Open questions
        active_questions = self.question_tracker.get_active_context(max_questions=5)
        context['open_questions'] = [q.question for q in active_questions]

        # Reviewer's emotional journey
        recent_emotions = reviewer_state.emotional_states[-5:] if reviewer_state.emotional_states else []
        context['my_recent_feelings'] = [
            {
                'scene': e.scene_number,
                'engagement': e.engagement_level,
                'enjoyment': e.enjoyment,
                'reaction': e.reaction
            }
            for e in recent_emotions
        ]

        return context

    def _build_scene_prompt(self, scene: Scene, reviewer_state: ReviewerState, context: Dict) -> str:
        """Build the prompt for the AI to review this scene"""

        prompt_parts = []

        # Context summary
        if context['recent_scenes']:
            prompt_parts.append("RECENT SCENES YOU REMEMBER:")
            for recent in context['recent_scenes'][-3:]:  # Last 3
                prompt_parts.append(f"  Scene {recent['scene_number']}: {recent['heading']}")
            prompt_parts.append("")

        if context['earlier_summaries']:
            prompt_parts.append("EARLIER IN THE SCRIPT:")
            for summary in context['earlier_summaries']:
                prompt_parts.append(f"  {summary}")
            prompt_parts.append("")

        if context['key_characters']:
            prompt_parts.append("KEY CHARACTERS:")
            for char in context['key_characters']:
                prompt_parts.append(f"  {char['name']} - appears often, seems important")
            prompt_parts.append("")

        if context['open_questions']:
            prompt_parts.append("QUESTIONS YOU'RE WONDERING ABOUT:")
            for q in context['open_questions']:
                prompt_parts.append(f"  - {q}")
            prompt_parts.append("")

        if context['my_recent_feelings']:
            prompt_parts.append("HOW YOU'VE BEEN FEELING:")
            for feeling in context['my_recent_feelings'][-3:]:
                engagement = "engaged" if feeling['engagement'] > 0.6 else "bored" if feeling['engagement'] < 0.4 else "neutral"
                enjoyment = "loving it" if feeling['enjoyment'] > 0.6 else "not enjoying" if feeling['enjoyment'] < 0.4 else "it's okay"
                prompt_parts.append(f"  Scene {feeling['scene']}: {engagement}, {enjoyment}")
            prompt_parts.append("")

        # The current scene
        prompt_parts.append("NOW YOU'RE READING:")
        prompt_parts.append(f"Scene {scene.scene_number}: {scene.heading}")
        prompt_parts.append("")
        prompt_parts.append(scene.full_text)
        prompt_parts.append("")

        # Request structured response
        prompt_parts.append("RESPOND WITH:")
        prompt_parts.append("1. Your reaction to this scene (2-3 sentences, natural and honest)")
        prompt_parts.append("2. Engagement (0-1): how engaged you feel")
        prompt_parts.append("3. Enjoyment (-1 to 1): how much you're enjoying this")
        prompt_parts.append("4. Any questions this raises for you")
        prompt_parts.append("5. Any questions that got answered")
        prompt_parts.append("")
        prompt_parts.append("Be authentic to your personality. Don't be overly positive or negative - react naturally.")

        return "\n".join(prompt_parts)

    def _parse_feedback_response(self, response: str, scene: Scene, reviewer_state: ReviewerState) -> SceneFeedback:
        """
        Parse AI response into structured feedback

        For now, simple parsing. Could enhance with structured output later.
        """
        # Extract engagement and enjoyment (look for patterns)
        engagement = 0.5
        enjoyment = 0.5

        lines = response.lower().split('\n')
        for line in lines:
            if 'engagement' in line:
                # Try to extract number
                import re
                match = re.search(r'(\d+\.?\d*)', line)
                if match:
                    engagement = float(match.group(1))
                    if engagement > 1:
                        engagement = engagement / 10  # Normalize if given as 0-10

            if 'enjoyment' in line:
                import re
                match = re.search(r'(-?\d+\.?\d*)', line)
                if match:
                    enjoyment = float(match.group(1))
                    if enjoyment > 1:
                        enjoyment = enjoyment / 10

        # Create emotional state
        emotional_state = EmotionalState(
            scene_number=scene.scene_number,
            engagement_level=engagement,
            enjoyment=enjoyment,
            reaction=response  # Store full response as reaction
        )

        return SceneFeedback(
            scene_number=scene.scene_number,
            reviewer_id=reviewer_state.reviewer_id,
            reviewer_name=reviewer_state.profile.name,
            feedback=response,
            emotional_state=emotional_state
        )

    def _update_memory(self, scene: Scene):
        """Update memory system after processing a scene"""
        # Build scene data
        scene_data = {
            "scene_id": scene.scene_id,
            "scene_number": scene.scene_number,
            "heading": scene.heading,
            "full_text": scene.full_text,
            "characters": scene.characters_present,
            "word_count": scene.word_count
        }

        # If memory full, compress oldest
        digest = None
        if self.memory.recent_memory.is_full():
            oldest = self.memory.recent_memory.scenes[0]

            # Get all reviewers' emotional states for this scene
            emotional_states = {}
            for reviewer_id, reviewer_state in self.reviewers.items():
                for emotion in reviewer_state.emotional_states:
                    if emotion.scene_number == oldest['scene_number']:
                        emotional_states[reviewer_id] = emotion.dict()
                        break

            # Create scene object for compression
            from models.screenplay import Scene as SceneModel
            oldest_scene = SceneModel(**oldest)

            # Compress with emotional data
            digest = self.compressor.compress_scene(oldest_scene, emotional_states)

        # Add to memory
        self.memory.add_scene(scene_data, digest=digest)
