"""
Test feedback engine - Phase 2

IMPORTANT: This test requires an Anthropic API key.
Set ANTHROPIC_API_KEY environment variable before running.

This is a DEMO test that will use the API (costs money).
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.parser import FountainParser
from services.entity_tracker import EntityTrackingService
from services.ai_provider import AIProviderFactory
from services.feedback_engine import FeedbackEngine
import os


def test_feedback_engine_demo():
    """
    Demo test - processes first 3 scenes of test screenplay with AI reviewers

    This COSTS MONEY (uses real API calls) - only run when intentional
    """

    print("=" * 60)
    print("FEEDBACK ENGINE DEMO - USING REAL AI")
    print("=" * 60)
    print()

    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  No ANTHROPIC_API_KEY found in environment")
        print("⚠️  This test requires a real API key and will cost money")
        print()
        print("To run this test:")
        print("1. Get API key from https://console.anthropic.com")
        print("2. Set environment variable: export ANTHROPIC_API_KEY='your-key'")
        print("3. Run test again")
        print()
        print("Skipping test.")
        return

    print("✓ API key found")
    print()

    # Parse test screenplay (first 3 scenes only)
    screenplay_path = Path(__file__).parent / "test_screenplay.fountain"

    if not screenplay_path.exists():
        print(f"✗ Test screenplay not found: {screenplay_path}")
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

    # Create AI provider
    print("Initializing Anthropic AI provider...")
    ai_provider = AIProviderFactory.create(
        "anthropic",
        model="claude-3-5-haiku-20241022"
    )
    print(f"✓ Using model: {ai_provider.get_model_name()}")
    print()

    # Create feedback engine with 2 reviewers
    print("Creating feedback engine with 2 reviewers...")
    engine = FeedbackEngine(
        ai_provider=ai_provider,
        reviewer_profiles=["blockbuster_fan", "indie_critic"]
    )
    print(f"✓ Reviewers: {', '.join([r.profile.name for r in engine.reviewers.values()])}")
    print()

    # Process first 3 scenes only (to save money)
    print("⚠️  Processing FIRST 3 SCENES ONLY (to limit API costs)")
    print()

    limited_screenplay = screenplay
    limited_screenplay.scenes = screenplay.scenes[:3]
    limited_screenplay.total_scenes = 3

    # Run review
    print("Starting review session...")
    print("This will make real API calls and cost money.")
    print()

    session = engine.review_screenplay(
        screenplay=limited_screenplay,
        entity_tracker=tracker
    )

    # Show results
    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print()

    for feedback in session.all_feedback:
        print(f"\nScene {feedback.scene_number} - {feedback.reviewer_name}")
        print("-" * 60)
        print(feedback.feedback)
        print()
        print(f"Engagement: {feedback.emotional_state.engagement_level:.2f}")
        print(f"Enjoyment: {feedback.emotional_state.enjoyment:.2f}")
        print()

    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print()
    print(f"Total scenes reviewed: {session.total_scenes}")
    print(f"Total feedback items: {len(session.all_feedback)}")
    print(f"Reviewers: {len(session.reviewers)}")
    print()
    print("Phase 2 feedback engine working! 🎉")


if __name__ == "__main__":
    test_feedback_engine_demo()
