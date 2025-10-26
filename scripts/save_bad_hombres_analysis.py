"""
Save Bad Hombres analysis for future reference

This script will:
1. Parse Bad Hombres screenplay
2. Run analysis with Jordan Peele and Sam Raimi
3. Save to analysis storage
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from services.parser import ScreenplayParser
from services.feedback_engine import FeedbackEngine
from services.analysis_storage import AnalysisStorage


def main():
    print("\n🎬 Saving Bad Hombres Analysis")
    print("=" * 60)

    # Paths
    screenplay_path = "SAMPLES/Screenplays/Bad Hombres by Filup Molina.pdf"

    # Check if file exists
    if not Path(screenplay_path).exists():
        print(f"⚠️  Screenplay not found: {screenplay_path}")
        return

    # Parse screenplay
    print("\n📄 Parsing screenplay...")
    parser = ScreenplayParser()
    screenplay = parser.parse_file(screenplay_path)
    print(f"✓ Parsed {len(screenplay.scenes)} scenes")

    # Generate feedback
    print("\n🧠 Generating feedback...")
    print("  Reviewers: Jordan Peele, Sam Raimi")

    engine = FeedbackEngine()

    # Jordan Peele feedback
    print("  Running Jordan Peele analysis...")
    jordan_feedback = []
    for scene in screenplay.scenes[:10]:  # First 10 scenes for demo
        fb = engine.generate_feedback(
            scene=scene,
            reviewer_name="Jordan Peele",
            screenplay_context=screenplay
        )
        jordan_feedback.append(fb)

    # Sam Raimi feedback
    print("  Running Sam Raimi analysis...")
    sam_feedback = []
    for scene in screenplay.scenes[:10]:
        fb = engine.generate_feedback(
            scene=scene,
            reviewer_name="Sam Raimi",
            screenplay_context=screenplay
        )
        sam_feedback.append(fb)

    all_feedback = jordan_feedback + sam_feedback
    print(f"✓ Generated {len(all_feedback)} feedback items")

    # Save to storage
    print("\n💾 Saving analysis...")
    storage = AnalysisStorage()
    filepath = storage.save_analysis(
        screenplay=screenplay,
        feedback=all_feedback,
        reviewers=["Jordan Peele", "Sam Raimi"],
        metadata={
            "notes": "First saved analysis - demo with first 10 scenes"
        }
    )

    print("\n" + "=" * 60)
    print("✅ Analysis saved successfully!")
    print(f"   File: {filepath}")
    print("\nTo load this analysis later:")
    print("  from services.analysis_storage import AnalysisStorage")
    print("  storage = AnalysisStorage()")
    print("  analysis = storage.load_analysis('bad-hombres-by-filup-molina')")


if __name__ == "__main__":
    main()
