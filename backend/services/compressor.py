"""
Scene compression service

Compresses full scenes to ~20% size digests (plot only)
Emotional data is NEVER compressed
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from models.screenplay import Scene
from models.memory import SceneDigest
from models.entity import EntityTracker
from typing import List, Dict


class SceneCompressor:
    """
    Compresses scenes into digests

    In production, this would use AI to generate intelligent summaries.
    For now, uses heuristic-based compression.
    """

    def __init__(self, entity_tracker: EntityTracker = None):
        self.entity_tracker = entity_tracker

    def compress_scene(self, scene: Scene,
                      emotional_states: Dict[str, dict] = None,
                      questions_raised: List[str] = None,
                      questions_answered: List[str] = None) -> SceneDigest:
        """
        Compress scene to digest

        Args:
            scene: Full scene object
            emotional_states: Dict of {reviewer_id: emotional_state}
            questions_raised: List of question IDs raised in this scene
            questions_answered: List of question IDs answered in this scene

        Returns:
            SceneDigest with compressed plot but full emotional data
        """
        # Generate summary (in production, would use AI)
        summary = self._generate_summary(scene)

        # Extract key objects mentioned
        key_objects = self._extract_key_objects(scene)

        # Identify plot beats
        plot_beats = self._identify_plot_beats(scene)

        # Calculate scene importance
        importance = self._calculate_scene_importance(scene)

        digest = SceneDigest(
            scene_id=scene.scene_id,
            scene_number=scene.scene_number,
            summary=summary,
            characters_present=scene.characters_present,
            key_objects=key_objects,
            plot_beats=plot_beats,
            importance_score=importance,
            emotional_states_by_reviewer=emotional_states or {},
            questions_raised=questions_raised or [],
            questions_answered=questions_answered or []
        )

        return digest

    def _generate_summary(self, scene: Scene) -> str:
        """
        Generate compressed summary of scene

        In production: Use AI to create intelligent summary
        For now: Use heuristics
        """
        # Extract key dialogue (first and last exchanges)
        dialogue_elements = [e for e in scene.elements if e.type == "dialogue"]

        summary_parts = []

        # Add location
        summary_parts.append(f"{scene.location}.")

        # Add character actions
        if scene.characters_present:
            chars = ", ".join(scene.characters_present[:3])
            if len(scene.characters_present) > 3:
                chars += f" and {len(scene.characters_present) - 3} others"
            summary_parts.append(f"{chars} present.")

        # Add key dialogue snippets
        if dialogue_elements:
            if len(dialogue_elements) >= 2:
                first_dialogue = dialogue_elements[0].text[:50]
                last_dialogue = dialogue_elements[-1].text[:50]
                summary_parts.append(f'Dialogue: "{first_dialogue}..." to "{last_dialogue}..."')
            else:
                dialogue = dialogue_elements[0].text[:100]
                summary_parts.append(f'"{dialogue}..."')

        # Add action description (first action line)
        action_elements = [e for e in scene.elements if e.type == "action"]
        if action_elements:
            action = action_elements[0].text[:80]
            summary_parts.append(f"Action: {action}...")

        summary = " ".join(summary_parts)

        # Compress to ~20% (very rough heuristic)
        if len(summary) > len(scene.full_text) * 0.3:
            summary = summary[:int(len(scene.full_text) * 0.2)] + "..."

        return summary

    def _extract_key_objects(self, scene: Scene) -> List[str]:
        """
        Extract key objects mentioned in scene

        In production: Use NER (Named Entity Recognition) or AI
        For now: Look for all-caps words that aren't characters
        """
        import re

        objects = []
        text = scene.full_text

        # Find all-caps words (potential objects)
        caps_words = re.findall(r'\b([A-Z]{2,}(?:\s+[A-Z]{2,})*)\b', text)

        for word in caps_words:
            # Filter out characters
            if word in scene.characters_present:
                continue
            # Filter out scene heading words
            if word in ['INT', 'EXT', 'DAY', 'NIGHT', 'CONTINUOUS', 'LATER']:
                continue
            # Filter out dialogue markers
            if word in ['V.O.', 'O.S.', "CONT'D"]:
                continue

            if word not in objects:
                objects.append(word)

        return objects[:5]  # Top 5 objects

    def _identify_plot_beats(self, scene: Scene) -> List[str]:
        """
        Identify plot beats in scene

        In production: Use AI to understand narrative structure
        For now: Use keyword detection
        """
        beats = []
        text = scene.full_text.lower()

        # Keyword-based beat detection (very basic)
        beat_keywords = {
            "revelation": ["reveal", "discover", "realize", "truth", "secret"],
            "conflict": ["argue", "fight", "confront", "challenge", "accuse"],
            "decision": ["decide", "choose", "must", "will"],
            "emotional": ["cry", "laugh", "smile", "tears", "angry", "sad"],
            "action": ["run", "chase", "escape", "attack", "defend"],
            "setup": ["plan", "prepare", "ready", "scheme"],
            "mystery": ["question", "wonder", "suspicious", "strange", "weird"]
        }

        for beat_type, keywords in beat_keywords.items():
            if any(keyword in text for keyword in keywords):
                beats.append(beat_type)

        return beats

    def _calculate_scene_importance(self, scene: Scene) -> float:
        """
        Calculate importance of this scene

        Factors:
        - Number of characters (more = potentially more important)
        - Dialogue density (more dialogue = more important)
        - Length (longer scenes often more significant)
        - Entity importance (if high-importance entities present)
        """
        score = 0.0

        # Character count (0.3 weight)
        char_count_score = min(len(scene.characters_present) / 5.0, 1.0) * 0.3
        score += char_count_score

        # Dialogue density (0.3 weight)
        dialogue_count = sum(1 for e in scene.elements if e.type == "dialogue")
        dialogue_score = min(dialogue_count / 10.0, 1.0) * 0.3
        score += dialogue_score

        # Length (0.2 weight)
        length_score = min(scene.word_count / 200.0, 1.0) * 0.2
        score += length_score

        # Entity importance (0.2 weight)
        if self.entity_tracker:
            high_importance_chars = [
                char for char in scene.characters_present
                if self.entity_tracker.find_entity_by_name(char) and
                   self.entity_tracker.find_entity_by_name(char).is_high_importance()
            ]
            entity_score = min(len(high_importance_chars) / 2.0, 1.0) * 0.2
            score += entity_score

        return min(score, 1.0)

    def batch_compress(self, scenes: List[Scene],
                      emotional_states_by_scene: Dict[str, Dict[str, dict]] = None) -> List[SceneDigest]:
        """
        Compress multiple scenes at once

        Args:
            scenes: List of scenes to compress
            emotional_states_by_scene: Dict of {scene_id: {reviewer_id: emotional_state}}

        Returns:
            List of SceneDigests
        """
        digests = []

        for scene in scenes:
            emotional_states = None
            if emotional_states_by_scene and scene.scene_id in emotional_states_by_scene:
                emotional_states = emotional_states_by_scene[scene.scene_id]

            digest = self.compress_scene(scene, emotional_states=emotional_states)
            digests.append(digest)

        return digests
