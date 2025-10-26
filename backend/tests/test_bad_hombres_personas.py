"""
Test Bad Hombres with multiple diverse personas

Processes first 5 scenes of Bad Hombres with:
- Genre specialists
- Industry professionals
- Craft-focused reviewers

COSTS MONEY - Real API calls
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


def test_bad_hombres_diverse_personas():
    """
    Test Bad Hombres (first 5 scenes) with diverse personas:

    GENRE SPECIALISTS:
    - Kane (Thriller Junkie)
    - Asher (Sci-Fi Nerd) - to see how they react to NON-scifi

    INDUSTRY PROFESSIONALS:
    - Casey Park (Script Reader) - brutal coverage
    - Alex Chen (Dev Exec) - marketability
    - Taylor Brooks (Showrunner) - series potential

    CRAFT-FOCUSED:
    - Ren Sasaki (Director POV) - visual storytelling
    - Aria Santos (Actor POV) - actable roles
    """

    print("=" * 60)
    print("BAD HOMBRES - DIVERSE PERSONA TEST")
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

    # Parse Bad Hombres PDF
    pdf_path = Path(__file__).parent.parent.parent / "Bad Hombres by Filup Molina.pdf"
    if not pdf_path.exists():
        print(f"✗ Bad Hombres PDF not found")
        return

    print(f"Parsing: {pdf_path.name}")
    print("(First 5 scenes only to save costs)")
    parser = FountainParser()

    # Parse just enough pages to get ~5 scenes
    screenplay = parser.parse_file(str(pdf_path), max_pages=10)
    print(f"✓ Parsed {screenplay.total_scenes} scenes from {parser.pdf_metadata['extracted_pages']} pages")
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

    # Create feedback engine with 7 diverse personas
    print("Creating feedback engine with 7 DIVERSE PERSONAS:")
    print()

    reviewer_configs = [
        # Genre specialists
        {"profile": "thriller_junkie", "ai_provider": "anthropic"},
        {"profile": "scifi_nerd", "ai_provider": "anthropic"},
        # Industry professionals
        {"profile": "script_reader", "ai_provider": "anthropic"},
        {"profile": "dev_exec", "ai_provider": "anthropic"},
        {"profile": "showrunner", "ai_provider": "anthropic"},
        # Craft-focused
        {"profile": "director_pov", "ai_provider": "anthropic"},
        {"profile": "actor_pov", "ai_provider": "anthropic"},
    ]

    engine = FeedbackEngine(
        ai_providers={"anthropic": ai_provider},
        reviewer_configs=reviewer_configs
    )

    print("Reviewers:")
    for reviewer_id, reviewer in engine.reviewers.items():
        print(f"  • {reviewer.profile.name}")
    print()

    # Process first 5 scenes only
    print("⚠️  Processing FIRST 5 SCENES ONLY (to limit API costs)")
    print()

    limited_screenplay = screenplay
    limited_screenplay.scenes = screenplay.scenes[:5]
    limited_screenplay.total_scenes = 5

    # Run review
    print("Starting review session...")
    print("This will make multiple API calls.")
    print()

    session = engine.review_screenplay(
        screenplay=limited_screenplay,
        entity_tracker=tracker
    )

    # Show results grouped by reviewer
    print()
    print("=" * 60)
    print("RESULTS - DIVERSE PERSPECTIVES ON BAD HOMBRES")
    print("=" * 60)
    print()

    # Group feedback by reviewer
    reviewers = [
        ("Kane (Thriller Junkie)", "thriller_junkie_anthropic"),
        ("Asher (Sci-Fi Nerd)", "scifi_nerd_anthropic"),
        ("Casey Park (Script Reader)", "script_reader_anthropic"),
        ("Alex Chen (Dev Exec)", "dev_exec_anthropic"),
        ("Taylor Brooks (Showrunner)", "showrunner_anthropic"),
        ("Ren Sasaki (Director POV)", "director_pov_anthropic"),
        ("Aria Santos (Actor POV)", "actor_pov_anthropic"),
    ]

    for name, reviewer_id in reviewers:
        print(f"\n{'='*60}")
        print(f"{name}")
        print(f"{'='*60}\n")

        reviewer_feedback = [f for f in session.all_feedback if f.reviewer_id == reviewer_id]

        # Show first and last scene feedback
        if reviewer_feedback:
            first = reviewer_feedback[0]
            last = reviewer_feedback[-1]

            print(f"Scene {first.scene_number} (first impression):")
            print(f"  {first.feedback[:200]}...")
            print(f"  Engagement: {first.emotional_state.engagement_level:.2f}")
            print(f"  Enjoyment: {first.emotional_state.enjoyment:.2f}")
            print()

            if len(reviewer_feedback) > 1:
                print(f"Scene {last.scene_number} (after reading more):")
                print(f"  {last.feedback[:200]}...")
                print(f"  Engagement: {last.emotional_state.engagement_level:.2f}")
                print(f"  Enjoyment: {last.emotional_state.enjoyment:.2f}")
                print()

    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print()
    print(f"✓ Processed 5 scenes with 7 different perspectives")
    print(f"✓ Total unique feedback items: {len(session.all_feedback)}")
    print()
    print("Notice how:")
    print("  • Thriller junkie focuses on tension")
    print("  • Sci-fi nerd notices when it's NOT sci-fi")
    print("  • Script reader is brutally efficient")
    print("  • Dev exec thinks marketability")
    print("  • Showrunner thinks series potential")
    print("  • Director thinks visually")
    print("  • Actor thinks actable roles")
    print()


if __name__ == "__main__":
    test_bad_hombres_diverse_personas()
