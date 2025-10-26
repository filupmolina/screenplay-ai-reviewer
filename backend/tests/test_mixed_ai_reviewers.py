"""
Test mixed AI reviewers - same personality, different AI brains

This demonstrates the concept:
- Max-Claude vs Max-GPT (same blockbuster fan personality, different AI)
- Morgan-Claude vs Morgan-GPT (same indie critic personality, different AI)

REQUIRES: Both Anthropic and OpenAI API keys
COSTS MONEY: Real API calls
"""
import sys
from pathlib import Path
import os

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.parser import FountainParser
from services.entity_tracker import EntityTrackingService
from services.ai_provider import AIProviderFactory
from services.feedback_engine import FeedbackEngine


def test_mixed_ai_reviewers():
    """
    Test same personality with different AI brains

    Creates 4 reviewers:
    1. Max (Blockbuster Fan) - Claude brain
    2. Max (Blockbuster Fan) - GPT brain
    3. Morgan (Indie Critic) - Claude brain
    4. Morgan (Indie Critic) - GPT brain
    """

    print("=" * 60)
    print("MIXED AI REVIEWERS TEST")
    print("=" * 60)
    print()

    # Check for both API keys
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not anthropic_key:
        print("⚠️  No ANTHROPIC_API_KEY found")
        print("Skipping test.")
        return

    if not openai_key:
        print("⚠️  No OPENAI_API_KEY found")
        print("Skipping test.")
        return

    print("✓ Both API keys found")
    print()

    # Parse test screenplay
    screenplay_path = Path(__file__).parent / "test_screenplay.fountain"
    if not screenplay_path.exists():
        print(f"✗ Test screenplay not found")
        return

    print(f"Parsing: {screenplay_path.name}")
    parser = FountainParser()
    screenplay = parser.parse_file(str(screenplay_path))
    print(f"✓ Parsed {screenplay.total_scenes} scenes")
    print()

    # Build entity tracker
    print("Building entity tracker...")
    tracker_service = EntityTrackingService()
    tracker = tracker_service.process_screenplay(screenplay)
    tracker_service.detect_key_moments(screenplay)
    tracker_service.detect_relationships(screenplay)
    tracker_service.assign_narrative_functions()
    print(f"✓ Tracked {len(tracker.entities)} entities")
    print()

    # Create both AI providers
    print("Initializing AI providers...")
    anthropic = AIProviderFactory.create("anthropic", model="claude-3-5-haiku-20241022")
    openai = AIProviderFactory.create("openai", model="gpt-4-turbo-preview")
    print(f"✓ Claude: {anthropic.get_model_name()}")
    print(f"✓ GPT: {openai.get_model_name()}")
    print()

    # Create feedback engine with mixed reviewers
    print("Creating feedback engine with MIXED reviewers...")
    print("Each personality gets BOTH AI brains:")
    print()

    reviewer_configs = [
        # Max (Blockbuster Fan) - both brains
        {"profile": "blockbuster_fan", "ai_provider": "anthropic"},
        {"profile": "blockbuster_fan", "ai_provider": "openai"},
        # Morgan (Indie Critic) - both brains
        {"profile": "indie_critic", "ai_provider": "anthropic"},
        {"profile": "indie_critic", "ai_provider": "openai"},
    ]

    engine = FeedbackEngine(
        ai_providers={
            "anthropic": anthropic,
            "openai": openai
        },
        reviewer_configs=reviewer_configs
    )

    print(f"✓ Created {len(engine.reviewers)} reviewers:")
    for reviewer_id, reviewer in engine.reviewers.items():
        print(f"  - {reviewer.profile.name} ({reviewer.ai_provider_name.upper()} brain)")
    print()

    # Process first 2 scenes only (to save money)
    print("⚠️  Processing FIRST 2 SCENES ONLY (to limit API costs)")
    print()

    limited_screenplay = screenplay
    limited_screenplay.scenes = screenplay.scenes[:2]
    limited_screenplay.total_scenes = 2

    # Run review
    print("Starting review session...")
    print("This will make API calls to BOTH Claude and GPT.")
    print()

    session = engine.review_screenplay(
        screenplay=limited_screenplay,
        entity_tracker=tracker
    )

    # Show results - compare same personality, different brains
    print()
    print("=" * 60)
    print("RESULTS - COMPARING SAME PERSONALITY, DIFFERENT BRAINS")
    print("=" * 60)
    print()

    # Group by scene and personality
    for scene_num in range(1, 3):
        print(f"\n{'='*60}")
        print(f"SCENE {scene_num}")
        print(f"{'='*60}")

        # Max (Blockbuster Fan) - Claude vs GPT
        print(f"\n--- MAX (BLOCKBUSTER FAN) ---\n")

        max_claude = [f for f in session.all_feedback
                      if f.scene_number == scene_num
                      and f.reviewer_id == "blockbuster_fan_anthropic"][0]

        max_gpt = [f for f in session.all_feedback
                   if f.scene_number == scene_num
                   and f.reviewer_id == "blockbuster_fan_openai"][0]

        print("CLAUDE BRAIN:")
        print(f"  {max_claude.feedback[:200]}...")
        print(f"  Engagement: {max_claude.emotional_state.engagement_level:.2f}")
        print(f"  Enjoyment: {max_claude.emotional_state.enjoyment:.2f}")
        print()

        print("GPT BRAIN:")
        print(f"  {max_gpt.feedback[:200]}...")
        print(f"  Engagement: {max_gpt.emotional_state.engagement_level:.2f}")
        print(f"  Enjoyment: {max_gpt.emotional_state.enjoyment:.2f}")
        print()

        # Morgan (Indie Critic) - Claude vs GPT
        print(f"--- MORGAN (INDIE CRITIC) ---\n")

        morgan_claude = [f for f in session.all_feedback
                         if f.scene_number == scene_num
                         and f.reviewer_id == "indie_critic_anthropic"][0]

        morgan_gpt = [f for f in session.all_feedback
                      if f.scene_number == scene_num
                      and f.reviewer_id == "indie_critic_openai"][0]

        print("CLAUDE BRAIN:")
        print(f"  {morgan_claude.feedback[:200]}...")
        print(f"  Engagement: {morgan_claude.emotional_state.engagement_level:.2f}")
        print(f"  Enjoyment: {morgan_claude.emotional_state.enjoyment:.2f}")
        print()

        print("GPT BRAIN:")
        print(f"  {morgan_gpt.feedback[:200]}...")
        print(f"  Engagement: {morgan_gpt.emotional_state.engagement_level:.2f}")
        print(f"  Enjoyment: {morgan_gpt.emotional_state.enjoyment:.2f}")
        print()

    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print()
    print(f"✓ Same personality, different AI brains = MORE DIVERSITY!")
    print(f"✓ Total unique perspectives: {len(session.all_feedback)}")
    print()


if __name__ == "__main__":
    test_mixed_ai_reviewers()
