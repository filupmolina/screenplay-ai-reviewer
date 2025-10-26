"""
Test entity tracking system
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.parser import FountainParser
from services.entity_tracker import EntityTrackingService


def test_entity_tracker():
    """Test entity tracking on test screenplay"""

    # Parse screenplay
    parser = FountainParser()
    test_file = Path(__file__).parent / 'test_screenplay.fountain'
    screenplay = parser.parse_file(str(test_file))

    # Track entities
    tracker_service = EntityTrackingService()
    tracker = tracker_service.process_screenplay(screenplay)

    # Detect relationships and key moments
    tracker_service.detect_key_moments(screenplay)
    tracker_service.detect_relationships(screenplay)
    tracker_service.assign_narrative_functions()

    print("=" * 60)
    print("ENTITY TRACKING TEST")
    print("=" * 60)

    # Get summary
    summary = tracker_service.get_analysis_summary()
    print(f"\nTotal Entities: {summary['total_entities']}")
    print(f"Characters: {summary['characters']}")
    print(f"Locations: {summary['locations']}")
    print(f"Key Moments: {summary['key_moments_total']}")
    print(f"Relationships: {summary['relationships_total']}")

    print("\n" + "=" * 60)
    print("IMPORTANCE GROUPS")
    print("=" * 60)

    for level in ["high", "medium", "low"]:
        entities = summary['importance_groups'][level]
        print(f"\n{level.upper()} Importance ({len(entities)}):")
        for name in entities:
            print(f"  - {name}")

    print("\n" + "=" * 60)
    print("DETAILED CHARACTER ANALYSIS")
    print("=" * 60)

    characters = [e for e in tracker.entities.values() if e.entity_type.value == "character"]
    characters.sort(key=lambda x: x.importance_score, reverse=True)

    for char in characters:
        print(f"\n{char.name} ({char.entity_id})")
        print(f"  Importance Score: {char.importance_score:.3f}")
        print(f"  Narrative Function: {char.narrative_function or 'unknown'}")
        print(f"  Appearances: {char.total_appearances} scenes (#{char.first_appearance}-#{char.last_appearance})")
        print(f"  Speaking: {char.speaking_lines} lines in {char.dialogue_count} exchanges")

        if char.relationships:
            print(f"  Relationships: {len(char.relationships)}")
            for rel in char.relationships[:3]:  # Show first 3
                print(f"    - {rel.relationship_type} with {rel.entity_name}")

        if char.key_moments:
            print(f"  Key Moments: {len(char.key_moments)}")
            for moment in char.key_moments:
                print(f"    - Scene {moment.scene_number} [{moment.significance}]: {moment.moment}")

    # Test the "forgotten maid" problem
    print("\n" + "=" * 60)
    print("'FORGOTTEN MAID' PROBLEM TEST")
    print("=" * 60)

    maid = tracker.find_entity_by_name("MAID") or tracker.find_entity_by_name("MARIA")
    if maid:
        print(f"\n✓ Maid/Maria tracked successfully!")
        print(f"  Entity ID: {maid.entity_id}")
        print(f"  Importance Score: {maid.importance_score:.3f}")
        print(f"  Importance Level: {'HIGH' if maid.is_high_importance() else 'MEDIUM' if maid.is_medium_importance() else 'LOW'}")
        print(f"  First Appearance: Scene {maid.first_appearance}")
        print(f"  Last Appearance: Scene {maid.last_appearance}")
        print(f"  Total Appearances: {maid.total_appearances}")
        print(f"  All Scenes: {maid.appearances}")

        if maid.is_high_importance():
            print(f"\n  ✓ MAID is HIGH importance - will NEVER be forgotten!")
        elif maid.is_medium_importance():
            print(f"\n  ⚠ MAID is MEDIUM importance - included when relevant")
        else:
            print(f"\n  ⚠ MAID is LOW importance - might need importance boost")

        print(f"\n  Relationships: {len(maid.relationships)}")
        for rel in maid.relationships:
            print(f"    - Connected to {rel.entity_name}")

    else:
        print("\n✗ Maid not found! This is the 'forgotten maid' problem!")

    print("\n" + "=" * 60)
    print("HIGH IMPORTANCE ENTITIES (ALWAYS IN CONTEXT)")
    print("=" * 60)

    high_importance = tracker.get_high_importance_entities()
    print(f"\nThese {len(high_importance)} entities will ALWAYS be included in AI context:")
    for entity in high_importance:
        print(f"  - {entity.name} (score: {entity.importance_score:.3f})")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

    # Assertions
    assert summary['characters'] >= 4, f"Expected at least 4 characters, got {summary['characters']}"
    assert maid is not None, "MAID/MARIA must be tracked"
    assert maid.total_appearances == 3, f"MARIA should appear in 3 scenes (merged MAID), got {maid.total_appearances}"
    assert maid.importance_score >= 0.4, f"MARIA should be at least medium importance, got {maid.importance_score:.3f}"
    assert "MAID" in maid.aliases or "THE MAID" in maid.aliases, "MARIA should have MAID as alias"

    print("\n✓ All assertions passed!")


if __name__ == "__main__":
    test_entity_tracker()
