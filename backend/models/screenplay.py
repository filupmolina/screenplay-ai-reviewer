"""
Screenplay data models
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class SceneElement(BaseModel):
    """Individual element within a scene (action, dialogue, etc)"""
    type: str  # action, character, dialogue, parenthetical, transition, scene_heading
    text: str
    line_number: Optional[int] = None


class Scene(BaseModel):
    """A single scene in the screenplay"""
    scene_number: int
    scene_id: str  # e.g., "SCENE_001"
    heading: str  # Full scene heading (e.g., "INT. MANSION - LIBRARY - NIGHT")
    location: Optional[str] = None  # Extracted location (e.g., "MANSION - LIBRARY")
    time_of_day: Optional[str] = None  # DAY, NIGHT, etc.
    interior_exterior: Optional[str] = None  # INT, EXT

    elements: List[SceneElement] = Field(default_factory=list)
    full_text: str  # Complete scene text

    characters_present: List[str] = Field(default_factory=list)
    characters_speaking: List[str] = Field(default_factory=list)

    word_count: int = 0
    page_start: Optional[int] = None
    page_end: Optional[int] = None


class Screenplay(BaseModel):
    """Complete screenplay structure"""
    title: Optional[str] = None
    author: Optional[str] = None
    draft_date: Optional[str] = None

    scenes: List[Scene] = Field(default_factory=list)

    total_scenes: int = 0
    total_pages: Optional[int] = None
    characters: List[str] = Field(default_factory=list)  # All unique characters
    word_count: int = 0

    metadata: Dict = Field(default_factory=dict)

    def get_scene_by_id(self, scene_id: str) -> Optional[Scene]:
        """Get a scene by its ID"""
        for scene in self.scenes:
            if scene.scene_id == scene_id:
                return scene
        return None

    def get_scene_by_number(self, scene_number: int) -> Optional[Scene]:
        """Get a scene by its number"""
        for scene in self.scenes:
            if scene.scene_number == scene_number:
                return scene
        return None

    def get_character_scenes(self, character: str) -> List[Scene]:
        """Get all scenes where a character appears"""
        return [
            scene for scene in self.scenes
            if character in scene.characters_present
        ]
