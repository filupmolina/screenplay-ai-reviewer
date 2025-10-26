"""
Test question tracking system
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from models.question import QuestionTracker, NarrativeWeight, QuestionStatus
from services.entity_tracker import EntityTrackingService
from services.parser import FountainParser


def test_question_tracker():
    """Test question tracking system"""

    print("=" * 60)
    print("QUESTION TRACKING TEST")
    print("=" * 60)

    # Create question tracker
    tracker = QuestionTracker()

    # Parse screenplay and track entities (for importance scoring)
    parser = FountainParser()
    test_file = Path(__file__).parent / 'test_screenplay.fountain'
    screenplay = parser.parse_file(str(test_file))

    entity_service = EntityTrackingService()
    entity_tracker = entity_service.process_screenplay(screenplay)

    # Simulate questions being raised as we watch the screenplay
    print("\n--- Scene 1: LIBRARY ---")
    q1 = tracker.add_question(
        question_text="Why is the maid eavesdropping? Is this intentional?",
        scene_number=1,
        reviewer_id="THE_MAINSTREAM",
        narrative_weight=NarrativeWeight.MEDIUM,
        related_entities=["CHARACTER_003"],  # MARIA
        speculation="She might be more than just a maid"
    )
    print(f"  Raised {q1.question_id}: {q1.question}")
    print(f"    Importance: {q1.importance_score:.3f}")

    print("\n--- Scene 2: BEDROOM ---")
    q2 = tracker.add_question(
        question_text="What's in the will? Why did father change it?",
        scene_number=2,
        reviewer_id="THE_MAINSTREAM",
        narrative_weight=NarrativeWeight.HIGH,
        speculation="This will is central to the conflict"
    )
    print(f"  Raised {q2.question_id}: {q2.question}")

    q3 = tracker.add_question(
        question_text="Will John prove himself worthy?",
        scene_number=2,
        reviewer_id="THE_ARTISTE",
        narrative_weight=NarrativeWeight.LOW,
        speculation="Character development arc"
    )
    print(f"  Raised {q3.question_id}: {q3.question}")

    print("\n--- Scene 3: HALLWAY ---")
    # Maid is listening again - reference Q1
    q1.add_reference(3)
    print(f"  Referenced {q1.question_id} (maid eavesdropping again)")
    print(f"    Importance increased to: {q1.importance_score:.3f}")
    print(f"    Urgency increased to: {q1.urgency:.3f}")

    print("\n--- Scene 4: KITCHEN ---")
    # MAJOR REVEAL - Maid is scheming with lawyer
    q1.add_reference(4)
    print(f"  Referenced {q1.question_id} (maid meeting lawyer secretly)")
    print(f"    Importance: {q1.importance_score:.3f}")

    # This partially answers the maid question
    q1.mark_answered(
        scene_number=4,
        answer="The maid (Maria) is conspiring with the lawyer. She's been playing a long game for 20 years."
    )
    print(f"  ANSWERED {q1.question_id}!")
    print(f"    Answer: {q1.answer[:60]}...")

    # New question raised
    q4 = tracker.add_question(
        question_text="What is Maria's endgame? What does she want?",
        scene_number=4,
        reviewer_id="THE_MAINSTREAM",
        narrative_weight=NarrativeWeight.CRITICAL,
        related_entities=["CHARACTER_003"],
        speculation="This feels like the main mystery now"
    )
    print(f"  Raised {q4.question_id}: {q4.question}")

    print("\n--- Scene 5: DINING ROOM ---")
    # Reference the will question
    q2.add_reference(5)
    q4.add_reference(5)  # Maria's plan still mysterious

    # Update all importance scores
    tracker.update_all_importance_scores(current_scene=5, entity_tracker=entity_tracker)

    # Show current state
    print("\n" + "=" * 60)
    print("QUESTION TRACKER STATE (After Scene 5)")
    print("=" * 60)

    status_summary = tracker.get_status_summary()
    print(f"\nStatus Summary:")
    print(f"  Open: {status_summary['open']}")
    print(f"  Answered: {status_summary['answered']}")
    print(f"  Irrelevant: {status_summary['irrelevant']}")

    importance_summary = tracker.get_importance_summary()
    print(f"\nImportance Groups (Open Questions):")
    print(f"  High (>0.7): {len(importance_summary['high'])} questions")
    print(f"  Medium (0.4-0.7): {len(importance_summary['medium'])} questions")
    print(f"  Low (<0.4): {len(importance_summary['low'])} questions")

    print("\n--- All Questions ---")
    for question_id, question in tracker.questions.items():
        status_icon = "✓" if question.status == QuestionStatus.ANSWERED else "?" if question.status == QuestionStatus.OPEN else "✗"
        print(f"\n{status_icon} {question_id} [{question.status.value}] (importance: {question.importance_score:.3f})")
        print(f"  Q: {question.question}")
        print(f"  Raised: Scene {question.raised_in_scene} by {question.raised_by_reviewer}")
        print(f"  Weight: {question.narrative_weight.value}, Urgency: {question.urgency:.2f}")
        print(f"  References: {len(question.references)} scenes {question.references}")

        if question.status == QuestionStatus.ANSWERED:
            print(f"  ✓ Answered in Scene {question.answered_in_scene}: {question.answer[:80]}...")
        elif question.status == QuestionStatus.IRRELEVANT:
            print(f"  ✗ Became irrelevant: {question.irrelevant_reason}")

    # Test active context (what to include in AI prompt)
    print("\n" + "=" * 60)
    print("ACTIVE CONTEXT (for AI prompt)")
    print("=" * 60)

    active_questions = tracker.get_active_context(max_questions=5)
    print(f"\nTop {len(active_questions)} most important open questions:")
    for i, q in enumerate(active_questions, 1):
        print(f"  {i}. [{q.importance_score:.3f}] {q.question}")

    # Test high importance filter
    print("\n" + "=" * 60)
    print("HIGH IMPORTANCE QUESTIONS (ALWAYS IN CONTEXT)")
    print("=" * 60)

    high_importance = tracker.get_high_importance_questions()
    if high_importance:
        print(f"\n{len(high_importance)} questions will ALWAYS be in AI context:")
        for q in high_importance:
            print(f"  - [{q.importance_score:.3f}] {q.question}")
    else:
        print("\nNo high-importance questions yet")
        print("(Questions gain importance through references and narrative weight)")

    # Test reviewer-specific questions
    print("\n" + "=" * 60)
    print("REVIEWER-SPECIFIC QUESTIONS")
    print("=" * 60)

    mainstream_questions = tracker.get_questions_by_reviewer("THE_MAINSTREAM")
    print(f"\nTHE_MAINSTREAM raised {len(mainstream_questions)} questions:")
    for q in mainstream_questions:
        print(f"  - {q.question_id}: {q.question[:60]}...")

    artiste_questions = tracker.get_questions_by_reviewer("THE_ARTISTE")
    print(f"\nTHE_ARTISTE raised {len(artiste_questions)} questions:")
    for q in artiste_questions:
        print(f"  - {q.question_id}: {q.question[:60]}...")

    # Assertions
    print("\n" + "=" * 60)
    print("ASSERTIONS")
    print("=" * 60)

    assert len(tracker.questions) == 4, f"Expected 4 questions, got {len(tracker.questions)}"
    assert status_summary['open'] == 3, f"Expected 3 open, got {status_summary['open']}"
    assert status_summary['answered'] == 1, f"Expected 1 answered, got {status_summary['answered']}"

    # Q1 should be answered
    assert q1.status == QuestionStatus.ANSWERED, "Q1 should be answered"
    assert q1.answered_in_scene == 4, "Q1 should be answered in scene 4"

    # Q4 (critical question about Maria's endgame) should have high importance
    assert q4.narrative_weight == NarrativeWeight.CRITICAL, "Q4 should be critical"

    # Questions should have references
    assert len(q1.references) >= 3, f"Q1 should have 3+ references, got {len(q1.references)}"

    print("\n✓ All assertions passed!")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_question_tracker()
