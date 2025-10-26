"""
Test memory management system
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from services.parser import FountainParser
from services.entity_tracker import EntityTrackingService
from services.compressor import SceneCompressor
from models.memory import MemoryManager


def test_memory_system():
    """Test sliding window memory system"""

    print("=" * 60)
    print("MEMORY SYSTEM TEST")
    print("=" * 60)

    # Parse screenplay
    parser = FountainParser()
    test_file = Path(__file__).parent / 'test_screenplay.fountain'
    screenplay = parser.parse_file(str(test_file))

    # Track entities
    tracker_service = EntityTrackingService()
    tracker = tracker_service.process_screenplay(screenplay)

    # Create compressor with entity tracker
    compressor = SceneCompressor(entity_tracker=tracker)

    # Create memory manager
    memory = MemoryManager()

    print(f"\nProcessing {screenplay.total_scenes} scenes...")
    print(f"Recent memory capacity: {memory.recent_memory.max_size} scenes\n")

    # Process scenes one by one (simulating real-time analysis)
    for scene in screenplay.scenes:
        print(f"\n--- Processing {scene.scene_id}: {scene.heading} ---")

        # Create scene data for memory
        scene_data = {
            "scene_id": scene.scene_id,
            "scene_number": scene.scene_number,
            "heading": scene.heading,
            "full_text": scene.full_text,
            "characters": scene.characters_present,
            "word_count": scene.word_count
        }

        # Simulate emotional states from reviewers
        emotional_states = {
            "THE_MAINSTREAM": {
                "primary_emotion": "intrigued",
                "intensity": 0.7,
                "cumulative_feelings": f"Scene {scene.scene_number}: Following along..."
            },
            "THE_ARTISTE": {
                "primary_emotion": "analytical",
                "intensity": 0.6,
                "cumulative_feelings": f"Scene {scene.scene_number}: Examining craft..."
            }
        }

        # If memory is full, compress the oldest scene
        digest = None
        if memory.recent_memory.is_full():
            # Get the scene that's about to be pushed out
            oldest_scene = memory.recent_memory.scenes[0]
            print(f"  ⚠ Recent memory full - compressing Scene {oldest_scene['scene_number']}")

            # Compress it
            oldest_scene_obj = screenplay.get_scene_by_number(oldest_scene['scene_number'])
            digest = compressor.compress_scene(
                oldest_scene_obj,
                emotional_states=emotional_states
            )

            print(f"    Original size: {len(oldest_scene['full_text'])} chars")
            print(f"    Compressed to: {len(digest.summary)} chars ({len(digest.summary)/len(oldest_scene['full_text'])*100:.1f}%)")
            print(f"    Importance: {digest.importance_score:.3f}")
            print(f"    Emotional data: {len(digest.emotional_states_by_reviewer)} reviewers (FULL data preserved)")

        # Add scene to memory
        memory.add_scene(scene_data, digest=digest)

        # Show current memory state
        print(f"  Memory state: {len(memory.recent_memory.scenes)} recent, {len(memory.historical_memory.digests)} historical")

    # Final memory state
    print("\n" + "=" * 60)
    print("FINAL MEMORY STATE")
    print("=" * 60)
    print(memory.get_context_summary())

    # Show recent scenes
    print("\n--- Recent Memory (Full Detail) ---")
    for scene_data in memory.get_recent_scenes():
        print(f"  Scene {scene_data['scene_number']}: {scene_data['heading']}")
        print(f"    {scene_data['word_count']} words, {len(scene_data['characters'])} characters")

    # Show historical digests
    print("\n--- Historical Memory (Compressed Digests) ---")
    for digest in memory.get_historical_digests():
        print(f"  Scene {digest.scene_number}: {digest.summary[:60]}...")
        print(f"    Importance: {digest.importance_score:.3f}")
        print(f"    Emotional states: {list(digest.emotional_states_by_reviewer.keys())}")
        print(f"    Plot beats: {', '.join(digest.plot_beats) if digest.plot_beats else 'none'}")

    # Test context retrieval
    print("\n" + "=" * 60)
    print("CONTEXT RETRIEVAL TEST")
    print("=" * 60)

    full_context = memory.get_full_context()
    print(f"Total scenes processed: {full_context['total_scenes_processed']}")
    print(f"Recent scenes: {full_context['recent_count']}")
    print(f"Historical digests: {full_context['historical_count']}")

    # Test reviewer-specific memory
    print("\n--- Reviewer-Specific Memory (THE_MAINSTREAM) ---")
    reviewer_memory = memory.get_memory_for_reviewer("THE_MAINSTREAM")
    emotional_journey = reviewer_memory['emotional_journey']
    print(f"Emotional journey: {len(emotional_journey)} historical scenes")
    for entry in emotional_journey:
        print(f"  Scene {entry['scene_number']}: {entry['emotional_state']['primary_emotion']} ({entry['emotional_state']['intensity']})")

    # Assertions
    print("\n" + "=" * 60)
    print("ASSERTIONS")
    print("=" * 60)

    total_scenes = screenplay.total_scenes
    assert memory.current_scene_number == total_scenes, f"Should have processed {total_scenes} scenes"

    # With 5 scene capacity and 5 total scenes, should have 5 recent, 0 historical
    expected_recent = min(total_scenes, memory.recent_memory.max_size)
    expected_historical = max(0, total_scenes - memory.recent_memory.max_size)

    actual_recent = len(memory.recent_memory.scenes)
    actual_historical = len(memory.historical_memory.digests)

    print(f"Expected: {expected_recent} recent, {expected_historical} historical")
    print(f"Actual: {actual_recent} recent, {actual_historical} historical")

    assert actual_recent == expected_recent, f"Expected {expected_recent} recent scenes, got {actual_recent}"
    assert actual_historical == expected_historical, f"Expected {expected_historical} historical, got {actual_historical}"

    # Verify emotional data preserved in digests
    for digest in memory.get_historical_digests():
        assert len(digest.emotional_states_by_reviewer) > 0, "Emotional states must be preserved"
        for reviewer_id, state in digest.emotional_states_by_reviewer.items():
            assert "primary_emotion" in state, "Must have emotional data"

    print("\n✓ All assertions passed!")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_memory_system()
