"""
Test screenplay parser
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.parser import FountainParser


def test_fountain_parser():
    """Test parsing the test screenplay"""
    parser = FountainParser()

    # Parse the test screenplay
    test_file = Path(__file__).parent / 'test_screenplay.fountain'
    screenplay = parser.parse_file(str(test_file))

    # Print results
    print("=" * 60)
    print("SCREENPLAY PARSING TEST")
    print("=" * 60)
    print(f"\nTitle: {screenplay.title}")
    print(f"Author: {screenplay.author}")
    print(f"Draft Date: {screenplay.draft_date}")
    print(f"\nTotal Scenes: {screenplay.total_scenes}")
    print(f"Total Characters: {len(screenplay.characters)}")
    print(f"Total Words: {screenplay.word_count}")

    print(f"\nAll Characters: {', '.join(screenplay.characters)}")

    print("\n" + "=" * 60)
    print("SCENE BREAKDOWN")
    print("=" * 60)

    for scene in screenplay.scenes:
        print(f"\n{scene.scene_id}: {scene.heading}")
        print(f"  Location: {scene.location}")
        print(f"  Time: {scene.time_of_day}")
        print(f"  Characters Present: {', '.join(scene.characters_present)}")
        print(f"  Characters Speaking: {', '.join(scene.characters_speaking)}")
        print(f"  Elements: {len(scene.elements)} ({', '.join([e.type for e in scene.elements[:5]])}...)")
        print(f"  Word Count: {scene.word_count}")

    # Test specific scene details
    print("\n" + "=" * 60)
    print("SCENE 1 DETAILED ANALYSIS")
    print("=" * 60)

    scene1 = screenplay.get_scene_by_number(1)
    if scene1:
        print(f"\nScene Heading: {scene1.heading}")
        print(f"\nElements ({len(scene1.elements)} total):")
        for i, element in enumerate(scene1.elements, 1):
            print(f"  {i}. [{element.type.upper()}] {element.text[:60]}{'...' if len(element.text) > 60 else ''}")

    # Test character scenes
    print("\n" + "=" * 60)
    print("MAID/MARIA APPEARANCES")
    print("=" * 60)

    maria_scenes = screenplay.get_character_scenes("MARIA")
    if not maria_scenes:
        maria_scenes = screenplay.get_character_scenes("MAID")

    print(f"\nFound in {len(maria_scenes)} scenes:")
    for scene in maria_scenes:
        print(f"  - {scene.scene_id}: {scene.heading}")
        speaking = "SPEAKING" if "MARIA" in scene.characters_speaking or "MAID" in scene.characters_speaking else "present only"
        print(f"    ({speaking})")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

    # Validate expectations
    assert screenplay.title == "The Forgotten Maid", f"Expected title 'The Forgotten Maid', got '{screenplay.title}'"
    assert screenplay.total_scenes == 5, f"Expected 5 scenes, got {screenplay.total_scenes}"
    assert "JOHN" in screenplay.characters, "JOHN should be in characters"
    assert "FATHER" in screenplay.characters, "FATHER should be in characters"
    assert "MARIA" in screenplay.characters or "MAID" in screenplay.characters, "MAID/MARIA should be in characters"

    print("\n✓ All assertions passed!")


if __name__ == "__main__":
    test_fountain_parser()
