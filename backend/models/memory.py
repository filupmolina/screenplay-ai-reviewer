"""
Memory models - sliding window with recent + historical
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from collections import deque


class SceneDigest(BaseModel):
    """
    Compressed scene summary (~20% of original size for plot)
    BUT 100% emotional data preserved
    """
    scene_id: str
    scene_number: int
    summary: str  # Compressed plot summary
    characters_present: List[str] = Field(default_factory=list)
    key_objects: List[str] = Field(default_factory=list)
    plot_beats: List[str] = Field(default_factory=list)  # revelation, conflict, etc.
    importance_score: float = 0.0

    # EMOTIONAL DATA - NEVER COMPRESSED
    emotional_states_by_reviewer: Dict[str, dict] = Field(default_factory=dict)

    # QUESTION TRACKING
    questions_raised: List[str] = Field(default_factory=list)  # Question IDs
    questions_answered: List[str] = Field(default_factory=list)  # Question IDs


class RecentMemory(BaseModel):
    """
    Recent detailed memory - last N scenes in full

    Uses deque for efficient sliding window
    """
    max_size: int = 5  # Last 5 scenes in detail
    scenes: List[dict] = Field(default_factory=list)  # Full scene data

    def add_scene(self, scene_data: dict):
        """Add scene to recent memory"""
        self.scenes.append(scene_data)

        # If over max size, oldest scene needs to be compressed
        if len(self.scenes) > self.max_size:
            return self.scenes.pop(0)  # Return oldest for compression
        return None

    def get_all_scenes(self) -> List[dict]:
        """Get all recent scenes"""
        return self.scenes

    def get_latest_scene(self) -> Optional[dict]:
        """Get most recent scene"""
        return self.scenes[-1] if self.scenes else None

    def is_full(self) -> bool:
        """Check if recent memory is at capacity"""
        return len(self.scenes) >= self.max_size


class HistoricalMemory(BaseModel):
    """
    Historical compressed memory - all older scenes as digests
    """
    digests: List[SceneDigest] = Field(default_factory=list)

    def add_digest(self, digest: SceneDigest):
        """Add compressed scene digest"""
        self.digests.append(digest)

    def get_all_digests(self) -> List[SceneDigest]:
        """Get all historical digests"""
        return self.digests

    def get_digest_by_scene(self, scene_id: str) -> Optional[SceneDigest]:
        """Get specific scene digest"""
        for digest in self.digests:
            if digest.scene_id == scene_id:
                return digest
        return None

    def get_digests_for_scenes(self, scene_ids: List[str]) -> List[SceneDigest]:
        """Get multiple digests"""
        return [d for d in self.digests if d.scene_id in scene_ids]


class MemoryManager(BaseModel):
    """
    Manages sliding window memory system

    - Recent: Last N scenes in full detail
    - Historical: Older scenes as compressed digests (BUT full emotional data)
    """
    recent_memory: RecentMemory = Field(default_factory=lambda: RecentMemory(max_size=5))
    historical_memory: HistoricalMemory = Field(default_factory=HistoricalMemory)

    current_scene_number: int = 0

    def add_scene(self, scene_data: dict, digest: Optional[SceneDigest] = None):
        """
        Add new scene to memory

        If recent memory is full, oldest scene gets compressed and moved to historical
        """
        self.current_scene_number = scene_data.get('scene_number', self.current_scene_number + 1)

        # Add to recent memory
        oldest_scene = self.recent_memory.add_scene(scene_data)

        # If recent memory pushed out a scene, add its digest to historical
        if oldest_scene and digest:
            self.historical_memory.add_digest(digest)

        return oldest_scene  # Return scene that needs compression (if any)

    def get_recent_scenes(self) -> List[dict]:
        """Get all recent scenes (full detail)"""
        return self.recent_memory.get_all_scenes()

    def get_historical_digests(self) -> List[SceneDigest]:
        """Get all historical digests"""
        return self.historical_memory.get_all_digests()

    def get_full_context(self) -> Dict:
        """
        Get complete memory context for AI

        Returns both recent (full) and historical (digests)
        """
        return {
            "recent_scenes": self.get_recent_scenes(),
            "historical_digests": [d.dict() for d in self.get_historical_digests()],
            "total_scenes_processed": self.current_scene_number,
            "recent_count": len(self.recent_memory.scenes),
            "historical_count": len(self.historical_memory.digests)
        }

    def get_context_summary(self) -> str:
        """Get human-readable summary of memory state"""
        recent_count = len(self.recent_memory.scenes)
        historical_count = len(self.historical_memory.digests)

        summary = f"Memory State (Scene {self.current_scene_number}):\n"
        summary += f"  Recent (full detail): {recent_count} scenes\n"
        summary += f"  Historical (digests): {historical_count} scenes\n"
        summary += f"  Total tracked: {recent_count + historical_count} scenes\n"

        if self.recent_memory.scenes:
            recent_scene_nums = [s.get('scene_number', '?') for s in self.recent_memory.scenes]
            summary += f"  Recent window: Scenes {recent_scene_nums}\n"

        return summary

    def get_memory_for_reviewer(self, reviewer_id: str) -> Dict:
        """
        Get memory context specific to a reviewer

        Includes their emotional journey through historical scenes
        """
        # Get all emotional states for this reviewer from historical memory
        reviewer_emotional_journey = []
        for digest in self.historical_memory.digests:
            if reviewer_id in digest.emotional_states_by_reviewer:
                reviewer_emotional_journey.append({
                    "scene_number": digest.scene_number,
                    "scene_id": digest.scene_id,
                    "emotional_state": digest.emotional_states_by_reviewer[reviewer_id]
                })

        return {
            "recent_scenes": self.get_recent_scenes(),
            "historical_digests": [d.dict() for d in self.get_historical_digests()],
            "emotional_journey": reviewer_emotional_journey,
            "current_scene": self.current_scene_number
        }
