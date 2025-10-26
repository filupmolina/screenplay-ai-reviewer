"""
Question tracking models - tracks open questions/mysteries
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum


class QuestionStatus(str, Enum):
    """Status of a question"""
    OPEN = "open"
    ANSWERED = "answered"
    IRRELEVANT = "irrelevant"


class NarrativeWeight(str, Enum):
    """How central this question is to the plot"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Question(BaseModel):
    """
    A question/mystery raised during screenplay

    Tracked until answered or proven irrelevant
    """
    question_id: str  # e.g., "Q_047"
    question: str  # The actual question text
    raised_in_scene: int
    raised_by_reviewer: str  # Which reviewer asked this

    status: QuestionStatus = QuestionStatus.OPEN
    importance_score: float = 0.0  # 0.0 to 1.0

    # Tracking
    references: List[int] = Field(default_factory=list)  # Scenes where question was mentioned/relevant
    related_entities: List[str] = Field(default_factory=list)  # Entity IDs related to this question

    # Metadata
    narrative_weight: NarrativeWeight = NarrativeWeight.MEDIUM
    urgency: float = 0.5  # How pressing this feels (increases over time if unanswered)
    reviewer_speculation: Optional[str] = None

    # Resolution
    answered_in_scene: Optional[int] = None
    answer: Optional[str] = None
    became_irrelevant_in_scene: Optional[int] = None
    irrelevant_reason: Optional[str] = None

    def update_importance(self, current_scene: int, entity_tracker=None) -> float:
        """
        Calculate importance score

        Factors:
        - Reference count (0.25)
        - Duration (0.15)
        - Narrative weight (0.30)
        - Entity importance (0.15)
        - Urgency (0.15)
        """
        # Reference count
        reference_count_score = min(len(self.references) / 5.0, 1.0) * 0.25

        # Duration weight (how long it's been open)
        if current_scene > self.raised_in_scene:
            duration = (current_scene - self.raised_in_scene) / current_scene
            duration_score = duration * 0.15
        else:
            duration_score = 0.0

        # Narrative weight
        narrative_weights = {
            NarrativeWeight.CRITICAL: 1.0,
            NarrativeWeight.HIGH: 0.75,
            NarrativeWeight.MEDIUM: 0.50,
            NarrativeWeight.LOW: 0.25
        }
        narrative_score = narrative_weights[self.narrative_weight] * 0.30

        # Entity importance
        entity_score = 0.0
        if entity_tracker and self.related_entities:
            max_entity_importance = max([
                entity_tracker.get_entity(entity_id).importance_score
                for entity_id in self.related_entities
                if entity_tracker.get_entity(entity_id)
            ] or [0.0])
            entity_score = max_entity_importance * 0.15

        # Urgency
        urgency_score = self.urgency * 0.15

        # Recency boost (recently mentioned)
        recency_boost = 0.0
        if self.references:
            last_reference = max(self.references)
            if (current_scene - last_reference) < 3:
                recency_boost = 0.10

        total = (reference_count_score + duration_score + narrative_score +
                entity_score + urgency_score + recency_boost)

        self.importance_score = min(total, 1.0)
        return self.importance_score

    def add_reference(self, scene_number: int):
        """Mark that this question was mentioned/relevant in a scene"""
        if scene_number not in self.references:
            self.references.append(scene_number)

            # Increase urgency if repeatedly referenced but not answered
            if self.status == QuestionStatus.OPEN:
                self.urgency = min(self.urgency + 0.1, 1.0)

    def mark_answered(self, scene_number: int, answer: str):
        """Mark question as answered"""
        self.status = QuestionStatus.ANSWERED
        self.answered_in_scene = scene_number
        self.answer = answer

    def mark_irrelevant(self, scene_number: int, reason: str):
        """Mark question as no longer relevant"""
        self.status = QuestionStatus.IRRELEVANT
        self.became_irrelevant_in_scene = scene_number
        self.irrelevant_reason = reason

    def is_high_importance(self) -> bool:
        """Check if question is high importance (>0.7)"""
        return self.importance_score > 0.7

    def is_medium_importance(self) -> bool:
        """Check if question is medium importance (0.4-0.7)"""
        return 0.4 <= self.importance_score <= 0.7

    def is_low_importance(self) -> bool:
        """Check if question is low importance (<0.4)"""
        return self.importance_score < 0.4


class QuestionTracker(BaseModel):
    """
    Tracks all questions across entire screenplay

    Prevents forgetting major mysteries
    """
    questions: Dict[str, Question] = Field(default_factory=dict)
    question_counter: int = 0

    def add_question(self, question_text: str, scene_number: int,
                    reviewer_id: str, narrative_weight: NarrativeWeight = NarrativeWeight.MEDIUM,
                    related_entities: List[str] = None,
                    speculation: str = None) -> Question:
        """Add a new question"""
        self.question_counter += 1
        question_id = f"Q_{self.question_counter:03d}"

        question = Question(
            question_id=question_id,
            question=question_text,
            raised_in_scene=scene_number,
            raised_by_reviewer=reviewer_id,
            narrative_weight=narrative_weight,
            related_entities=related_entities or [],
            reviewer_speculation=speculation,
            references=[scene_number]  # Question is referenced in the scene it's raised
        )

        self.questions[question_id] = question
        return question

    def get_question(self, question_id: str) -> Optional[Question]:
        """Get question by ID"""
        return self.questions.get(question_id)

    def get_open_questions(self) -> List[Question]:
        """Get all open questions"""
        return [q for q in self.questions.values() if q.status == QuestionStatus.OPEN]

    def get_high_importance_questions(self) -> List[Question]:
        """Get all high importance questions (>0.7)"""
        return [q for q in self.get_open_questions() if q.is_high_importance()]

    def get_questions_for_scene(self, scene_number: int) -> List[Question]:
        """Get questions that were referenced in a scene"""
        return [q for q in self.questions.values() if scene_number in q.references]

    def get_questions_by_reviewer(self, reviewer_id: str) -> List[Question]:
        """Get all questions raised by a specific reviewer"""
        return [q for q in self.questions.values() if q.raised_by_reviewer == reviewer_id]

    def update_all_importance_scores(self, current_scene: int, entity_tracker=None):
        """Update importance scores for all open questions"""
        for question in self.get_open_questions():
            question.update_importance(current_scene, entity_tracker)

    def get_importance_summary(self) -> Dict[str, List[str]]:
        """Get questions grouped by importance level"""
        open_questions = self.get_open_questions()
        return {
            "high": [q.question_id for q in open_questions if q.is_high_importance()],
            "medium": [q.question_id for q in open_questions if q.is_medium_importance()],
            "low": [q.question_id for q in open_questions if q.is_low_importance()]
        }

    def get_status_summary(self) -> Dict[str, int]:
        """Get count of questions by status"""
        return {
            "open": len([q for q in self.questions.values() if q.status == QuestionStatus.OPEN]),
            "answered": len([q for q in self.questions.values() if q.status == QuestionStatus.ANSWERED]),
            "irrelevant": len([q for q in self.questions.values() if q.status == QuestionStatus.IRRELEVANT])
        }

    def get_active_context(self, max_questions: int = 10) -> List[Question]:
        """
        Get the most important questions for current context

        Returns up to max_questions sorted by importance
        """
        open_questions = self.get_open_questions()
        open_questions.sort(key=lambda q: q.importance_score, reverse=True)
        return open_questions[:max_questions]

    def prune_low_importance(self, threshold: float = 0.2):
        """
        Archive very low importance questions

        Questions below threshold are marked as irrelevant
        """
        for question in self.get_open_questions():
            if question.importance_score < threshold:
                question.mark_irrelevant(
                    scene_number=question.references[-1] if question.references else question.raised_in_scene,
                    reason="Low importance - auto-pruned"
                )
