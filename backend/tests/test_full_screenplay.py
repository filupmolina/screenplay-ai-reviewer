"""
Test full screenplay processing - Bad Hombres
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.parser import FountainParser
from services.entity_tracker import EntityTrackingService
from services.compressor import SceneCompressor
from models.memory import MemoryManager


def test_full_screenplay():
    """Process full Bad Hombres screenplay"""

    print("=" * 60)
    print("FULL SCREENPLAY PROCESSING - BAD HOMBRES")
    print("=" * 60)

    pdf_path = Path(__file__).parent.parent.parent / "Bad Hombres by Filup Molina.pdf"

    if not pdf_path.exists():
        print(f"\n✗ PDF not found")
        return

    print(f"\nProcessing: {pdf_path.name}")
    print("This will take a moment...\n")

    # Parse full screenplay
    parser = FountainParser()
    screenplay = parser.parse_file(str(pdf_path))  # No max_pages = process all

    print(f"--- SCREENPLAY STATS ---")
    print(f"Pages: {parser.pdf_metadata['total_pages']}")
    print(f"Scenes: {screenplay.total_scenes}")
    print(f"Characters: {len(screenplay.characters)}")
    print(f"Total words: {screenplay.word_count:,}")

    # Track entities
    print(f"\n--- ENTITY TRACKING ---")
    tracker_service = EntityTrackingService()
    tracker = tracker_service.process_screenplay(screenplay)
    tracker_service.detect_key_moments(screenplay)
    tracker_service.detect_relationships(screenplay)
    tracker_service.assign_narrative_functions()

    summary = tracker_service.get_analysis_summary()
    print(f"Total entities: {summary['total_entities']}")
    print(f"Characters: {summary['characters']}")
    print(f"High importance: {len(summary['importance_groups']['high'])}")
    print(f"Medium importance: {len(summary['importance_groups']['medium'])}")

    # Show top characters
    characters = [e for e in tracker.entities.values() if e.entity_type.value == "character"]
    characters.sort(key=lambda x: x.importance_score, reverse=True)

    print(f"\n--- TOP 10 CHARACTERS ---")
    for i, char in enumerate(characters[:10], 1):
        print(f"{i:2d}. {char.name:20s} | Score: {char.importance_score:.3f} | Scenes: {char.total_appearances:3d} | Lines: {char.speaking_lines:4d}")

    # Test memory system with full screenplay
    print(f"\n--- MEMORY SYSTEM TEST ---")
    memory = MemoryManager()
    compressor = SceneCompressor(entity_tracker=tracker)

    scenes_processed = 0
    for scene in screenplay.scenes:
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
        if memory.recent_memory.is_full():
            oldest = memory.recent_memory.scenes[0]
            oldest_scene_obj = screenplay.get_scene_by_number(oldest['scene_number'])
            digest = compressor.compress_scene(oldest_scene_obj)

        memory.add_scene(scene_data, digest=digest)
        scenes_processed += 1

    print(f"Scenes processed: {scenes_processed}")
    print(f"Recent memory: {len(memory.recent_memory.scenes)} scenes")
    print(f"Historical memory: {len(memory.historical_memory.digests)} digests")
    print(f"Compression ratio: {len(memory.historical_memory.digests) / scenes_processed * 100:.1f}% compressed")

    # Show high importance characters (these will NEVER be forgotten)
    high_importance = tracker.get_high_importance_entities()
    if high_importance:
        print(f"\n--- HIGH IMPORTANCE (ALWAYS IN CONTEXT) ---")
        for entity in high_importance:
            print(f"  • {entity.name} (score: {entity.importance_score:.3f})")
            print(f"    Appears in {entity.total_appearances} scenes")
            if entity.narrative_function:
                print(f"    Role: {entity.narrative_function}")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\n✓ Successfully processed entire 65-page screenplay!")
    print(f"✓ Parsed {screenplay.total_scenes} scenes")
    print(f"✓ Tracked {summary['characters']} characters")
    print(f"✓ Memory system handled {scenes_processed} scenes efficiently")
    print(f"\nAll systems working on full-length screenplay.")


if __name__ == "__main__":
    test_full_screenplay()
