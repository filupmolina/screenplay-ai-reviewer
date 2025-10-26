"""
Entity tracking models - prevents "forgotten maid" problem
"""
from typing import List, Dict, Optional, Set
from pydantic import BaseModel, Field
from enum import Enum


class EntityType(str, Enum):
    """Types of entities we track"""
    CHARACTER = "character"
    OBJECT = "object"
    LOCATION = "location"
    RELATIONSHIP = "relationship"


class KeyMoment(BaseModel):
    """A significant moment involving this entity"""
    scene_id: str
    scene_number: int
    moment: str  # Description of what happened
    significance: str  # low, medium, high, critical


class Relationship(BaseModel):
    """Relationship between two entities"""
    entity_id: str
    entity_name: str
    relationship_type: str  # employer, friend, enemy, family, etc.
    tension: Optional[str] = None  # hidden_resentment, love, rivalry, etc.
    since_scene: Optional[int] = None


class Entity(BaseModel):
    """
    Tracked entity (character, object, location)

    Prevents plot-critical elements from being forgotten
    """
    entity_id: str  # e.g., "MAID_001", "WILL_001"
    entity_type: EntityType
    name: str
    aliases: List[str] = Field(default_factory=list)

    # Tracking
    first_appearance: int  # Scene number
    last_appearance: int
    appearances: List[int] = Field(default_factory=list)  # All scene numbers
    total_appearances: int = 0

    # For characters
    speaking_lines: int = 0
    dialogue_count: int = 0

    # Importance
    importance_score: float = 0.0  # 0.0 to 1.0

    # Narrative significance
    key_moments: List[KeyMoment] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)
    mentioned_when_absent: List[int] = Field(default_factory=list)  # Scenes discussed but not present
    narrative_function: Optional[str] = None  # protagonist, antagonist, mentor, etc.

    # Metadata
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    def update_importance(self, current_scene: int) -> float:
        """
        Recalculate importance score

        Based on:
        - Speaking lines (0.25)
        - Appearances (0.20)
        - Scene span (0.15)
        - Mentioned when absent (0.15)
        - Relationships (0.10)
        - Key moments (0.15)
        """
        # Speaking weight (adjusted for shorter screenplays)
        speaking_weight = min(self.speaking_lines / 10.0, 1.0) * 0.25

        # Appearance weight (adjusted for shorter screenplays)
        appearance_weight = min(self.total_appearances / 5.0, 1.0) * 0.20

        # Span weight (appears early and late = important)
        if current_scene > 0:
            span = (self.last_appearance - self.first_appearance) / current_scene
            span_weight = span * 0.15
        else:
            span_weight = 0.0

        # Mentioned when absent (people talk about them)
        mention_weight = min(len(self.mentioned_when_absent) / 5.0, 1.0) * 0.15

        # Relationship complexity
        relationship_weight = min(len(self.relationships) / 3.0, 1.0) * 0.10

        # Key moments
        critical_moments = sum(1 for m in self.key_moments if m.significance == "critical")
        high_moments = sum(1 for m in self.key_moments if m.significance == "high")
        key_moments_weight = min((critical_moments * 1.0 + high_moments * 0.5) / 3.0, 1.0) * 0.15

        # Recency bonus (appeared recently)
        recency_bonus = 0.10 if (current_scene - self.last_appearance) < 3 else 0.0

        total = (speaking_weight + appearance_weight + span_weight +
                mention_weight + relationship_weight + key_moments_weight + recency_bonus)

        self.importance_score = min(total, 1.0)
        return self.importance_score

    def add_appearance(self, scene_number: int, spoke: bool = False, lines: int = 0):
        """Record an appearance in a scene"""
        if scene_number not in self.appearances:
            self.appearances.append(scene_number)
            self.total_appearances = len(self.appearances)

        self.last_appearance = scene_number

        if spoke:
            self.speaking_lines += lines
            self.dialogue_count += 1

    def add_key_moment(self, scene_id: str, scene_number: int, moment: str, significance: str):
        """Add a significant moment"""
        self.key_moments.append(KeyMoment(
            scene_id=scene_id,
            scene_number=scene_number,
            moment=moment,
            significance=significance
        ))

    def add_relationship(self, entity_id: str, entity_name: str,
                        relationship_type: str, tension: Optional[str] = None,
                        since_scene: Optional[int] = None):
        """Add or update a relationship"""
        # Check if relationship exists
        for rel in self.relationships:
            if rel.entity_id == entity_id:
                rel.relationship_type = relationship_type
                rel.tension = tension
                return

        # New relationship
        self.relationships.append(Relationship(
            entity_id=entity_id,
            entity_name=entity_name,
            relationship_type=relationship_type,
            tension=tension,
            since_scene=since_scene or self.last_appearance
        ))

    def is_high_importance(self) -> bool:
        """Check if entity is high importance (>0.7)"""
        return self.importance_score > 0.7

    def is_medium_importance(self) -> bool:
        """Check if entity is medium importance (0.4-0.7)"""
        return 0.4 <= self.importance_score <= 0.7

    def is_low_importance(self) -> bool:
        """Check if entity is low importance (<0.4)"""
        return self.importance_score < 0.4


class EntityTracker(BaseModel):
    """
    Tracks all entities across entire screenplay

    Prevents the "forgotten maid" problem
    """
    entities: Dict[str, Entity] = Field(default_factory=dict)
    entity_counter: Dict[EntityType, int] = Field(default_factory=lambda: {
        EntityType.CHARACTER: 0,
        EntityType.OBJECT: 0,
        EntityType.LOCATION: 0,
        EntityType.RELATIONSHIP: 0
    })

    def add_entity(self, name: str, entity_type: EntityType,
                   first_scene: int, aliases: Optional[List[str]] = None) -> Entity:
        """Add a new entity"""
        # Check if entity already exists by name or alias
        existing = self.find_entity_by_name(name)
        if existing:
            return existing

        # Generate ID
        self.entity_counter[entity_type] += 1
        entity_id = f"{entity_type.value.upper()}_{self.entity_counter[entity_type]:03d}"

        entity = Entity(
            entity_id=entity_id,
            entity_type=entity_type,
            name=name,
            aliases=aliases or [],
            first_appearance=first_scene,
            last_appearance=first_scene,
            appearances=[first_scene],
            total_appearances=1
        )

        self.entities[entity_id] = entity
        return entity

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID"""
        return self.entities.get(entity_id)

    def find_entity_by_name(self, name: str) -> Optional[Entity]:
        """Find entity by name or alias"""
        name_upper = name.upper()
        for entity in self.entities.values():
            if entity.name.upper() == name_upper:
                return entity
            if name_upper in [alias.upper() for alias in entity.aliases]:
                return entity
        return None

    def get_or_create_character(self, name: str, scene_number: int) -> Entity:
        """Get existing character or create new one"""
        entity = self.find_entity_by_name(name)
        if entity:
            return entity
        return self.add_entity(name, EntityType.CHARACTER, scene_number)

    def update_all_importance_scores(self, current_scene: int):
        """Update importance scores for all entities"""
        for entity in self.entities.values():
            entity.update_importance(current_scene)

    def get_high_importance_entities(self) -> List[Entity]:
        """Get all high importance entities (>0.7)"""
        return [e for e in self.entities.values() if e.is_high_importance()]

    def get_entities_in_scene(self, scene_number: int) -> List[Entity]:
        """Get all entities that appear in a scene"""
        return [e for e in self.entities.values() if scene_number in e.appearances]

    def get_character_list(self) -> List[str]:
        """Get list of all character names"""
        return sorted([
            e.name for e in self.entities.values()
            if e.entity_type == EntityType.CHARACTER
        ])

    def get_importance_summary(self) -> Dict[str, List[str]]:
        """Get entities grouped by importance level"""
        return {
            "high": [e.name for e in self.entities.values() if e.is_high_importance()],
            "medium": [e.name for e in self.entities.values() if e.is_medium_importance()],
            "low": [e.name for e in self.entities.values() if e.is_low_importance()]
        }
