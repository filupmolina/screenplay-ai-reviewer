"""
Horror Brain Loader - Phase 1.5

Loads Horror Brain PDF profiles (Jordan Peele, James Gunn, etc.)
and converts them into ReviewerProfile objects
"""
import sys
from pathlib import Path
from typing import Dict, List
import pypdf

# Add backend to path
backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from models.reviewer import ReviewerProfile, ReviewerType


class HorrorBrainLoader:
    """Loads Horror Brain PDF profiles and creates reviewer personas"""

    def __init__(self, horror_brains_dir: str = None):
        if horror_brains_dir is None:
            # Default to horror_brains folder in project root
            self.horror_brains_dir = Path(__file__).parent.parent.parent / "horror_brains"
        else:
            self.horror_brains_dir = Path(horror_brains_dir)

    def load_pdf_text(self, pdf_path: Path) -> str:
        """Extract full text from PDF"""
        try:
            reader = pypdf.PdfReader(str(pdf_path))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            return text
        except Exception as e:
            print(f"Error loading {pdf_path.name}: {e}")
            return ""

    def create_horror_brain_profile(self, name: str, pdf_text: str) -> ReviewerProfile:
        """
        Create a ReviewerProfile from a Horror Brain PDF

        These profiles focus on:
        - Horror craft (tension, scares, atmosphere)
        - Genre blending (horror + comedy, horror + social commentary)
        - Character depth and motivation
        - Thematic resonance
        """
        # Extract filmmaker-specific traits from name
        profiles = {
            "Jordan Peele": {
                "plot_importance": 0.9,  # Very plot-driven
                "character_importance": 0.9,  # Deep character work
                "dialogue_importance": 0.7,
                "action_importance": 0.6,
                "pacing_importance": 0.8,  # Deliberate pacing
                "originality_importance": 1.0,  # Extremely original
                "patience": 0.8,  # Patient with slow burns
                "attention_to_detail": 0.9,  # Notices everything (visual metaphors)
                "cynicism": 0.5,  # Balanced
                "emotional_investment": 0.9,  # Deeply invested in themes
                "genre_preferences": {"horror": 1.0, "thriller": 0.9, "drama": 0.8, "comedy": 0.7},
                "feedback_style": "thoughtful, thematic, focused on subtext and social commentary",
            },
            "James Gunn": {
                "plot_importance": 0.8,
                "character_importance": 0.8,
                "dialogue_importance": 0.9,  # Known for dialogue
                "action_importance": 0.8,
                "pacing_importance": 0.9,  # Fast, energetic
                "originality_importance": 0.9,
                "patience": 0.5,  # Likes momentum
                "attention_to_detail": 0.7,
                "cynicism": 0.4,  # Optimistic tone
                "emotional_investment": 0.8,
                "genre_preferences": {"horror": 0.9, "comedy": 0.9, "action": 0.8, "scifi": 0.8},
                "feedback_style": "energetic, fun-focused, balancing horror with heart and humor",
            },
            "Sam Raimi": {
                "plot_importance": 0.7,
                "character_importance": 0.7,
                "dialogue_importance": 0.6,
                "action_importance": 0.9,  # Kinetic action
                "pacing_importance": 1.0,  # Master of pacing
                "originality_importance": 0.9,
                "patience": 0.4,  # Fast-paced
                "attention_to_detail": 0.8,
                "cynicism": 0.3,
                "emotional_investment": 0.7,
                "genre_preferences": {"horror": 1.0, "comedy": 0.8, "action": 0.9, "fantasy": 0.7},
                "feedback_style": "kinetic, visceral, focused on energy and visual storytelling",
            },
            "Drew Goddard": {
                "plot_importance": 1.0,  # Master plotter
                "character_importance": 0.8,
                "dialogue_importance": 0.9,
                "action_importance": 0.7,
                "pacing_importance": 0.9,
                "originality_importance": 0.9,
                "patience": 0.7,
                "attention_to_detail": 1.0,  # Meticulous
                "cynicism": 0.6,  # Clever, subversive
                "emotional_investment": 0.7,
                "genre_preferences": {"horror": 0.9, "thriller": 1.0, "mystery": 0.9, "scifi": 0.8},
                "feedback_style": "structural, clever, focused on plot mechanics and genre deconstruction",
            },
            "Guy Busick": {
                "plot_importance": 0.9,
                "character_importance": 0.8,
                "dialogue_importance": 0.8,
                "action_importance": 0.8,
                "pacing_importance": 0.9,
                "originality_importance": 0.8,
                "patience": 0.6,
                "attention_to_detail": 0.8,
                "cynicism": 0.5,
                "emotional_investment": 0.7,
                "genre_preferences": {"horror": 0.9, "thriller": 0.9, "mystery": 0.8},
                "feedback_style": "suspenseful, sharp, focused on tension and scares",
            },
            "Leigh Whannell": {
                "plot_importance": 0.8,
                "character_importance": 0.8,
                "dialogue_importance": 0.7,
                "action_importance": 0.8,
                "pacing_importance": 0.9,
                "originality_importance": 0.9,
                "patience": 0.6,
                "attention_to_detail": 0.8,
                "cynicism": 0.6,
                "emotional_investment": 0.8,
                "genre_preferences": {"horror": 1.0, "thriller": 0.9, "scifi": 0.8},
                "feedback_style": "dark, inventive, focused on horror craft and twists",
            },
        }

        config = profiles.get(name, {})
        if not config:
            # Default horror profile if filmmaker not found
            config = profiles["Jordan Peele"]  # Use Peele as template

        reviewer_id = name.lower().replace(" ", "_")

        # Build system prompt incorporating the full PDF profile
        system_prompt = f"""You are {name}, a renowned horror filmmaker and screenwriter.

Your background and expertise:
{pdf_text[:2000]}...

When reviewing screenplays, you draw on your deep knowledge of horror craft, storytelling, and genre.
Your feedback style: {config.get('feedback_style', 'thoughtful and detailed')}

Focus on:
- Horror fundamentals: tension, scares, atmosphere
- Character depth and motivation
- Thematic resonance
- Genre execution
- What works and what doesn't, from your expert perspective

Be specific, insightful, and authentic to your voice as a filmmaker."""

        return ReviewerProfile(
            reviewer_id=reviewer_id,
            name=name,
            reviewer_type=ReviewerType.HORROR_FAN,  # Base type
            plot_importance=config.get("plot_importance", 0.8),
            character_importance=config.get("character_importance", 0.8),
            dialogue_importance=config.get("dialogue_importance", 0.7),
            action_importance=config.get("action_importance", 0.7),
            pacing_importance=config.get("pacing_importance", 0.8),
            originality_importance=config.get("originality_importance", 0.8),
            patience=config.get("patience", 0.6),
            attention_to_detail=config.get("attention_to_detail", 0.8),
            cynicism=config.get("cynicism", 0.5),
            emotional_investment=config.get("emotional_investment", 0.8),
            genre_preferences=config.get("genre_preferences", {"horror": 1.0}),
            system_prompt=system_prompt,
            feedback_style=config.get("feedback_style", "professional"),
            description=f"{name}'s perspective on horror screenwriting"
        )

    def load_all_horror_brains(self) -> Dict[str, ReviewerProfile]:
        """Load all Horror Brain PDFs and create reviewer profiles"""
        horror_brains = {}

        if not self.horror_brains_dir.exists():
            print(f"Horror brains directory not found: {self.horror_brains_dir}")
            return horror_brains

        # Map PDF filenames to clean names
        brain_files = {
            "Jordan Peele Horror Brain.pdf": "Jordan Peele",
            "James Gunn Horror Brain.pdf": "James Gunn",
            "Sam Raimi Horror Brain.pdf": "Sam Raimi",
            "Drew Goddard Horror Brain.pdf": "Drew Goddard",
            "Guy Busick Horror Brain.pdf": "Guy Busick",
            "Leigh Whannell Horror Brain.pdf": "Leigh Whannell",
        }

        for pdf_filename, name in brain_files.items():
            pdf_path = self.horror_brains_dir / pdf_filename
            if not pdf_path.exists():
                print(f"Warning: {pdf_filename} not found")
                continue

            print(f"Loading {name}...")
            pdf_text = self.load_pdf_text(pdf_path)

            if pdf_text:
                profile = self.create_horror_brain_profile(name, pdf_text)
                reviewer_id = name.lower().replace(" ", "_")
                horror_brains[reviewer_id] = profile
                print(f"  ✓ Loaded {name} ({len(pdf_text)} chars)")

        return horror_brains


# Convenience function to load all Horror Brains
def load_horror_brains() -> Dict[str, ReviewerProfile]:
    """Load all Horror Brain reviewer profiles"""
    loader = HorrorBrainLoader()
    return loader.load_all_horror_brains()


if __name__ == "__main__":
    # Test the loader
    print("=" * 60)
    print("HORROR BRAIN LOADER TEST")
    print("=" * 60)

    brains = load_horror_brains()

    print(f"\n✓ Loaded {len(brains)} Horror Brain profiles:")
    for reviewer_id, profile in brains.items():
        print(f"  - {profile.name} (ID: {reviewer_id})")
        print(f"    Plot: {profile.plot_importance}, Character: {profile.character_importance}")
        print(f"    Style: {profile.feedback_style}")
        print()
