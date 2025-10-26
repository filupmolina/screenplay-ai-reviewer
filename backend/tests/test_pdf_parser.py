"""
Test PDF screenplay parsing
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.parser import FountainParser
from services.entity_tracker import EntityTrackingService


def test_pdf_parsing():
    """Test parsing PDF screenplay (first 3 pages only - SAFE)"""

    print("=" * 60)
    print("PDF SCREENPLAY PARSING TEST")
    print("=" * 60)

    # Path to PDF
    pdf_path = Path(__file__).parent.parent.parent / "Bad Hombres by Filup Molina.pdf"

    if not pdf_path.exists():
        print(f"\n✗ PDF not found at: {pdf_path}")
        return

    print(f"\nPDF: {pdf_path.name}")

    # Parse first 3 pages only (SAFE - won't blow context)
    parser = FountainParser()

    try:
        screenplay = parser.parse_file(str(pdf_path), max_pages=3)

        print(f"\n--- PARSING RESULTS ---")
        print(f"Title: {screenplay.title or 'Not detected'}")
        print(f"Author: {screenplay.author or 'Not detected'}")
        print(f"PDF pages processed: {parser.pdf_metadata['extracted_pages']}/{parser.pdf_metadata['total_pages']}")
        print(f"\nScenes found: {screenplay.total_scenes}")
        print(f"Characters found: {len(screenplay.characters)}")
        print(f"Total words: {screenplay.word_count}")

        print(f"\nAll characters: {', '.join(screenplay.characters)}")

        print("\n" + "=" * 60)
        print("SCENES")
        print("=" * 60)

        for scene in screenplay.scenes:
            print(f"\n{scene.scene_id}: {scene.heading}")
            print(f"  Location: {scene.location}")
            print(f"  Time: {scene.time_of_day}")
            print(f"  Characters: {', '.join(scene.characters_present)}")
            print(f"  Speaking: {', '.join(scene.characters_speaking)}")
            print(f"  Word count: {scene.word_count}")
            print(f"  Elements: {len(scene.elements)}")

        # Show first scene in detail
        if screenplay.scenes:
            print("\n" + "=" * 60)
            print("FIRST SCENE DETAILED")
            print("=" * 60)
            scene1 = screenplay.scenes[0]
            print(f"\nHeading: {scene1.heading}")
            print(f"\nFirst 300 chars of text:")
            print(scene1.full_text[:300])
            print("...")

        # Test entity tracking on PDF
        print("\n" + "=" * 60)
        print("ENTITY TRACKING")
        print("=" * 60)

        tracker_service = EntityTrackingService()
        tracker = tracker_service.process_screenplay(screenplay)
        tracker_service.detect_key_moments(screenplay)
        tracker_service.detect_relationships(screenplay)
        tracker_service.assign_narrative_functions()

        summary = tracker_service.get_analysis_summary()
        print(f"\nTotal entities: {summary['total_entities']}")
        print(f"Characters: {summary['characters']}")
        print(f"Locations: {summary['locations']}")

        print(f"\nImportance groups:")
        for level in ["high", "medium", "low"]:
            entities = summary['importance_groups'][level]
            if entities:
                print(f"  {level.upper()}: {', '.join(entities)}")

        # Show top 3 characters
        characters = [e for e in tracker.entities.values() if e.entity_type.value == "character"]
        characters.sort(key=lambda x: x.importance_score, reverse=True)

        print(f"\nTop 3 characters (by importance):")
        for i, char in enumerate(characters[:3], 1):
            print(f"  {i}. {char.name} (score: {char.importance_score:.3f})")
            print(f"     Appears in: {char.total_appearances} scenes")
            print(f"     Speaking lines: {char.speaking_lines}")

        print("\n" + "=" * 60)
        print("TEST COMPLETE")
        print("=" * 60)
        print(f"\n✓ Successfully parsed first 3 pages of 65-page screenplay!")
        print(f"✓ Found {screenplay.total_scenes} scenes")
        print(f"✓ Tracked {summary['characters']} characters")
        print(f"\nREADY to process full screenplay when needed.")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_pdf_parsing()
