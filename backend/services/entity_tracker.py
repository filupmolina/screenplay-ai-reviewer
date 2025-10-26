"""
Entity tracking service

Processes screenplay and tracks all entities
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from models.screenplay import Screenplay, Scene
from models.entity import EntityTracker, EntityType, Entity


class EntityTrackingService:
    """
    Service to track entities throughout a screenplay
    """

    def __init__(self):
        self.tracker = EntityTracker()

    def process_screenplay(self, screenplay: Screenplay) -> EntityTracker:
        """
        Process entire screenplay and build entity tracker

        Returns populated EntityTracker
        """
        for scene in screenplay.scenes:
            self.process_scene(scene)

        # Update all importance scores at the end
        final_scene = screenplay.scenes[-1].scene_number if screenplay.scenes else 0
        self.tracker.update_all_importance_scores(final_scene)

        return self.tracker

    def process_scene(self, scene: Scene):
        """
        Process a single scene, updating entity tracker
        """
        # Normalize character names (MAID = MARIA, etc)
        char_aliases = {
            "MAID": "MARIA",
            "THE MAID": "MARIA"
        }

        # Track characters who are speaking
        for char_name in scene.characters_speaking:
            # Check for aliases
            normalized_name = char_aliases.get(char_name.upper(), char_name)
            entity = self.tracker.get_or_create_character(normalized_name, scene.scene_number)

            # Add alias if different
            if normalized_name != char_name and char_name not in entity.aliases:
                entity.aliases.append(char_name)

            # Count dialogue lines for this character
            dialogue_lines = sum(
                1 for elem in scene.elements
                if elem.type == "dialogue" and self._previous_character_is(scene.elements, elem, char_name)
            )

            entity.add_appearance(
                scene_number=scene.scene_number,
                spoke=True,
                lines=dialogue_lines
            )

        # Track characters who are present but not speaking
        non_speaking = set(scene.characters_present) - set(scene.characters_speaking)
        for char_name in non_speaking:
            # Check for aliases
            normalized_name = char_aliases.get(char_name.upper(), char_name)
            entity = self.tracker.get_or_create_character(normalized_name, scene.scene_number)

            # Add alias if different
            if normalized_name != char_name and char_name not in entity.aliases:
                entity.aliases.append(char_name)

            entity.add_appearance(
                scene_number=scene.scene_number,
                spoke=False
            )

        # Track location if significant
        if scene.location:
            location = self.tracker.find_entity_by_name(scene.location)
            if not location:
                location = self.tracker.add_entity(
                    name=scene.location,
                    entity_type=EntityType.LOCATION,
                    first_scene=scene.scene_number
                )
            else:
                location.add_appearance(scene.scene_number)

    def _previous_character_is(self, elements, current_element, char_name: str) -> bool:
        """Check if the previous character element matches the given name"""
        current_idx = elements.index(current_element)

        # Look backwards for the most recent character element
        for i in range(current_idx - 1, -1, -1):
            if elements[i].type == "character":
                return elements[i].text.upper() == char_name.upper()

        return False

    def detect_key_moments(self, screenplay: Screenplay):
        """
        Detect key moments for entities (would use AI in real implementation)

        For now, use heuristics:
        - First appearance = potentially significant
        - Last appearance (if not recent) = potentially significant
        - Scenes where character appears after long absence
        """
        for entity_id, entity in self.tracker.entities.items():
            if entity.entity_type != EntityType.CHARACTER:
                continue

            # First appearance
            first_scene = screenplay.get_scene_by_number(entity.first_appearance)
            if first_scene:
                entity.add_key_moment(
                    scene_id=first_scene.scene_id,
                    scene_number=first_scene.scene_number,
                    moment=f"First appearance of {entity.name}",
                    significance="medium"
                )

            # Check for gaps in appearances (returns after absence)
            sorted_appearances = sorted(entity.appearances)
            for i in range(1, len(sorted_appearances)):
                gap = sorted_appearances[i] - sorted_appearances[i-1]
                if gap > 10:  # Absent for 10+ scenes
                    scene = screenplay.get_scene_by_number(sorted_appearances[i])
                    if scene:
                        entity.add_key_moment(
                            scene_id=scene.scene_id,
                            scene_number=scene.scene_number,
                            moment=f"{entity.name} returns after {gap} scene absence",
                            significance="high"
                        )

    def detect_relationships(self, screenplay: Screenplay):
        """
        Detect relationships between characters (heuristic-based)

        Real implementation would use AI to understand context
        """
        for scene in screenplay.scenes:
            # Characters in same scene multiple times = relationship
            chars_in_scene = scene.characters_present

            if len(chars_in_scene) >= 2:
                # For each pair of characters in the scene
                for i, char1_name in enumerate(chars_in_scene):
                    for char2_name in chars_in_scene[i+1:]:
                        char1 = self.tracker.find_entity_by_name(char1_name)
                        char2 = self.tracker.find_entity_by_name(char2_name)

                        if char1 and char2:
                            # Count shared scenes
                            shared_scenes = set(char1.appearances) & set(char2.appearances)

                            # If they appear together frequently, they have a relationship
                            if len(shared_scenes) >= 2:
                                # Add bidirectional relationship
                                char1.add_relationship(
                                    entity_id=char2.entity_id,
                                    entity_name=char2.name,
                                    relationship_type="associate",  # Generic, would use AI to detect type
                                    since_scene=min(shared_scenes)
                                )
                                char2.add_relationship(
                                    entity_id=char1.entity_id,
                                    entity_name=char1.name,
                                    relationship_type="associate",
                                    since_scene=min(shared_scenes)
                                )

    def assign_narrative_functions(self):
        """
        Assign narrative functions based on importance and appearance patterns

        Heuristic-based (real implementation would use AI)
        """
        high_importance = self.tracker.get_high_importance_entities()

        if not high_importance:
            return

        # Most important character is likely protagonist
        high_importance.sort(key=lambda e: e.importance_score, reverse=True)

        if high_importance:
            high_importance[0].narrative_function = "protagonist"

        # Characters with high importance but appear late might be antagonists
        for entity in high_importance[1:]:
            if entity.first_appearance > 3 and entity.importance_score > 0.75:
                entity.narrative_function = "antagonist_potential"
            elif len(entity.relationships) >= 2:
                entity.narrative_function = "supporting"

    def get_analysis_summary(self) -> dict:
        """Get summary of entity analysis"""
        importance_groups = self.tracker.get_importance_summary()

        return {
            "total_entities": len(self.tracker.entities),
            "characters": len([e for e in self.tracker.entities.values()
                             if e.entity_type == EntityType.CHARACTER]),
            "locations": len([e for e in self.tracker.entities.values()
                            if e.entity_type == EntityType.LOCATION]),
            "importance_groups": importance_groups,
            "high_importance_count": len(importance_groups["high"]),
            "key_moments_total": sum(len(e.key_moments) for e in self.tracker.entities.values()),
            "relationships_total": sum(len(e.relationships) for e in self.tracker.entities.values())
        }
