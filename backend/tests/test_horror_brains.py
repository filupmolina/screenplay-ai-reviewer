"""
Test Horror Brain personas integration
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from models.reviewer import REVIEWER_PROFILES


def test_horror_brains_loaded():
    """Verify Horror Brain profiles are loaded"""
    print("=" * 60)
    print("HORROR BRAIN INTEGRATION TEST")
    print("=" * 60)

    horror_brains = [
        "jordan_peele",
        "james_gunn",
        "sam_raimi",
        "drew_goddard",
        "guy_busick",
        "leigh_whannell",
    ]

    print(f"\n✓ Total reviewer profiles: {len(REVIEWER_PROFILES)}")
    print(f"\nVerifying Horror Brains are loaded...\n")

    all_loaded = True
    for brain_id in horror_brains:
        if brain_id in REVIEWER_PROFILES:
            profile = REVIEWER_PROFILES[brain_id]
            print(f"✓ {profile.name}")
            print(f"  - Plot importance: {profile.plot_importance}")
            print(f"  - Originality importance: {profile.originality_importance}")
            print(f"  - Feedback style: {profile.feedback_style}")
            print(f"  - System prompt length: {len(profile.system_prompt)} chars")
            print()
        else:
            print(f"✗ {brain_id} NOT FOUND")
            all_loaded = False

    if all_loaded:
        print("\n" + "=" * 60)
        print("SUCCESS: All 6 Horror Brain personas loaded!")
        print("=" * 60)
    else:
        print("\nFAILED: Some Horror Brains missing")

    return all_loaded


def test_horror_brain_profiles():
    """Check Horror Brain profile characteristics"""
    print("\n" + "=" * 60)
    print("HORROR BRAIN PROFILE ANALYSIS")
    print("=" * 60)

    horror_brains = ["jordan_peele", "james_gunn", "sam_raimi", "drew_goddard"]

    for brain_id in horror_brains:
        profile = REVIEWER_PROFILES[brain_id]
        print(f"\n{profile.name}:")
        print(f"  Type: {profile.reviewer_type.value}")
        print(f"  Patience: {profile.patience} (slow burn tolerance)")
        print(f"  Cynicism: {profile.cynicism}")
        print(f"  Emotional investment: {profile.emotional_investment}")
        print(f"  Attention to detail: {profile.attention_to_detail}")
        print(f"  Top genre: {max(profile.genre_preferences.items(), key=lambda x: x[1])}")


if __name__ == "__main__":
    success = test_horror_brains_loaded()
    if success:
        test_horror_brain_profiles()
