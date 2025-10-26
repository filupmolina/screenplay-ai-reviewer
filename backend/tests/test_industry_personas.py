"""
Test industry professional personas

Shows how different Casey Park (Script Reader) vs Alex Chen (Dev Exec)
vs Taylor Brooks (Showrunner) think about the same material
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


def test_industry_personas():
    """
    Test 3 industry personas on same scene:
    1. Casey Park (Script Reader) - brutal, efficient, seen everything
    2. Alex Chen (Dev Exec) - thinking marketability, pitch, star roles
    3. Taylor Brooks (Showrunner) - thinking series potential, character engines
    """

    print("=" * 60)
    print("INDUSTRY PROFESSIONAL PERSONAS TEST")
    print("=" * 60)
    print()

    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  No ANTHROPIC_API_KEY found")
        print("Skipping test.")
        return

    print("✓ API key found")
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

    # Create AI provider
    print("Initializing AI provider...")
    ai_provider = AIProviderFactory.create("anthropic", model="claude-3-5-haiku-20241022")
    print(f"✓ Using: {ai_provider.get_model_name()}")
    print()

    # Create feedback engine with 3 industry personas
    print("Creating feedback engine with INDUSTRY PROFESSIONALS:")
    print()

    reviewer_configs = [
        {"profile": "script_reader", "ai_provider": "anthropic"},
        {"profile": "dev_exec", "ai_provider": "anthropic"},
        {"profile": "showrunner", "ai_provider": "anthropic"},
    ]

    engine = FeedbackEngine(
        ai_providers={"anthropic": ai_provider},
        reviewer_configs=reviewer_configs
    )

    print("Reviewers:")
    for reviewer_id, reviewer in engine.reviewers.items():
        print(f"  - {reviewer.profile.name}")
        print(f"    {reviewer.profile.description}")
    print()

    # Process first 2 scenes only
    print("⚠️  Processing FIRST 2 SCENES ONLY (to limit API costs)")
    print()

    limited_screenplay = screenplay
    limited_screenplay.scenes = screenplay.scenes[:2]
    limited_screenplay.total_scenes = 2

    # Run review
    print("Starting review session...")
    print()

    session = engine.review_screenplay(
        screenplay=limited_screenplay,
        entity_tracker=tracker
    )

    # Show results - compare industry perspectives
    print()
    print("=" * 60)
    print("RESULTS - INDUSTRY PROFESSIONAL PERSPECTIVES")
    print("=" * 60)
    print()

    for scene_num in range(1, 3):
        print(f"\n{'='*60}")
        print(f"SCENE {scene_num}")
        print(f"{'='*60}\n")

        script_reader = [f for f in session.all_feedback
                         if f.scene_number == scene_num
                         and f.reviewer_id == "script_reader_anthropic"][0]

        dev_exec = [f for f in session.all_feedback
                    if f.scene_number == scene_num
                    and f.reviewer_id == "dev_exec_anthropic"][0]

        showrunner = [f for f in session.all_feedback
                      if f.scene_number == scene_num
                      and f.reviewer_id == "showrunner_anthropic"][0]

        print("CASEY PARK (SCRIPT READER) - Brutal, efficient:")
        print(f"  {script_reader.feedback[:250]}...")
        print(f"  Engagement: {script_reader.emotional_state.engagement_level:.2f}")
        print()

        print("ALEX CHEN (DEV EXEC) - Thinking marketability:")
        print(f"  {dev_exec.feedback[:250]}...")
        print(f"  Engagement: {dev_exec.emotional_state.engagement_level:.2f}")
        print()

        print("TAYLOR BROOKS (SHOWRUNNER) - Thinking series potential:")
        print(f"  {showrunner.feedback[:250]}...")
        print(f"  Engagement: {showrunner.emotional_state.engagement_level:.2f}")
        print()

    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print()
    print("✓ Industry personas provide TOTALLY different perspectives!")
    print("✓ Script reader: PASS or CONSIDER?")
    print("✓ Dev exec: Can I pitch this?")
    print("✓ Showrunner: Can this sustain 5 seasons?")
    print()


if __name__ == "__main__":
    test_industry_personas()
