"""
Analysis Storage - Save and load screenplay analyses

Stores:
- Parsed screenplay data
- Scene-by-scene feedback
- Emotional tracking
- Character analysis
- Metadata (date, reviewers, etc.)

Allows:
- Loading previous analyses
- Continuing conversations about past analyses
- Comparing analyses over time
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import asdict
import sys

sys.path.append(str(Path(__file__).parent.parent))

from models.screenplay import Screenplay
from models.reviewer import ReviewerFeedback


class AnalysisStorage:
    """
    Manages saving and loading screenplay analyses

    Storage format:
    data/analyses/
        {screenplay_slug}/
            {timestamp}_{reviewers}.json
            latest.json -> symlink to most recent
    """

    def __init__(self, storage_dir: str = "data/analyses"):
        """Initialize storage system"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_analysis(
        self,
        screenplay: Screenplay,
        feedback: List[ReviewerFeedback],
        reviewers: List[str],
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Save complete analysis

        Args:
            screenplay: Parsed screenplay
            feedback: List of reviewer feedback
            reviewers: Names of reviewers used
            metadata: Optional additional metadata

        Returns:
            Path to saved analysis file
        """

        # Create slug from screenplay title
        slug = self._create_slug(screenplay.title or "untitled")

        # Create directory for this screenplay
        screenplay_dir = self.storage_dir / slug
        screenplay_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reviewers_str = "_".join([r.replace(" ", "_") for r in reviewers])
        filename = f"{timestamp}_{reviewers_str}.json"
        filepath = screenplay_dir / filename

        # Build analysis data
        analysis_data = {
            "metadata": {
                "saved_at": timestamp,
                "screenplay_title": screenplay.title,
                "screenplay_slug": slug,
                "reviewers": reviewers,
                "version": "1.0",
                **(metadata or {})
            },
            "screenplay": self._serialize_screenplay(screenplay),
            "feedback": [self._serialize_feedback(fb) for fb in feedback]
        }

        # Save to file
        with open(filepath, 'w') as f:
            json.dump(analysis_data, f, indent=2)

        # Create/update "latest" symlink
        latest_path = screenplay_dir / "latest.json"
        if latest_path.exists() or latest_path.is_symlink():
            latest_path.unlink()
        latest_path.symlink_to(filename)

        print(f"✓ Saved analysis: {filepath}")

        return str(filepath)

    def load_analysis(
        self,
        screenplay_slug: str,
        version: str = "latest"
    ) -> Optional[Dict]:
        """
        Load analysis for a screenplay

        Args:
            screenplay_slug: Slug of screenplay
            version: "latest" or specific timestamp

        Returns:
            Analysis data or None if not found
        """

        screenplay_dir = self.storage_dir / screenplay_slug

        if not screenplay_dir.exists():
            print(f"⚠️  No analyses found for '{screenplay_slug}'")
            return None

        # Determine which file to load
        if version == "latest":
            filepath = screenplay_dir / "latest.json"
        else:
            # Find file matching timestamp
            matching_files = list(screenplay_dir.glob(f"{version}*.json"))
            if not matching_files:
                print(f"⚠️  No analysis found for version '{version}'")
                return None
            filepath = matching_files[0]

        if not filepath.exists():
            print(f"⚠️  Analysis file not found: {filepath}")
            return None

        # Load and return
        with open(filepath, 'r') as f:
            analysis_data = json.load(f)

        print(f"✓ Loaded analysis: {filepath}")
        print(f"  Title: {analysis_data['metadata']['screenplay_title']}")
        print(f"  Reviewers: {', '.join(analysis_data['metadata']['reviewers'])}")
        print(f"  Saved: {analysis_data['metadata']['saved_at']}")

        return analysis_data

    def list_analyses(self, screenplay_slug: Optional[str] = None) -> List[Dict]:
        """
        List all available analyses

        Args:
            screenplay_slug: Optional specific screenplay, or all if None

        Returns:
            List of analysis metadata
        """

        analyses = []

        if screenplay_slug:
            # List analyses for specific screenplay
            screenplay_dir = self.storage_dir / screenplay_slug
            if not screenplay_dir.exists():
                return []

            for filepath in sorted(screenplay_dir.glob("*.json")):
                if filepath.name == "latest.json":
                    continue

                with open(filepath, 'r') as f:
                    data = json.load(f)
                    analyses.append(data['metadata'])

        else:
            # List all analyses
            for screenplay_dir in sorted(self.storage_dir.iterdir()):
                if not screenplay_dir.is_dir():
                    continue

                for filepath in sorted(screenplay_dir.glob("*.json")):
                    if filepath.name == "latest.json":
                        continue

                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        analyses.append(data['metadata'])

        return analyses

    def list_screenplays(self) -> List[str]:
        """List all screenplays that have analyses"""
        screenplays = []

        for screenplay_dir in sorted(self.storage_dir.iterdir()):
            if screenplay_dir.is_dir():
                screenplays.append(screenplay_dir.name)

        return screenplays

    def _create_slug(self, title: str) -> str:
        """Create URL-safe slug from title"""
        import re

        # Convert to lowercase, replace spaces with hyphens
        slug = title.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars
        slug = re.sub(r'[-\s]+', '-', slug)  # Consolidate hyphens/spaces

        return slug

    def _serialize_screenplay(self, screenplay: Screenplay) -> Dict:
        """Convert screenplay to JSON-serializable dict"""
        return {
            "title": screenplay.title,
            "author": screenplay.author,
            "scenes": [
                {
                    "number": scene.number,
                    "heading": scene.heading,
                    "location": scene.location,
                    "time_of_day": scene.time_of_day,
                    "action_blocks": scene.action_blocks,
                    "dialogue_blocks": [
                        {
                            "character": d.character,
                            "parenthetical": d.parenthetical,
                            "text": d.text
                        }
                        for d in scene.dialogue_blocks
                    ]
                }
                for scene in screenplay.scenes
            ]
        }

    def _serialize_feedback(self, feedback: ReviewerFeedback) -> Dict:
        """Convert feedback to JSON-serializable dict"""
        return {
            "scene_number": feedback.scene_number,
            "reviewer_name": feedback.reviewer_name,
            "feedback_text": feedback.feedback_text,
            "emotional_state": feedback.emotional_state.value if feedback.emotional_state else None,
            "intensity": feedback.intensity,
            "character_insights": feedback.character_insights,
            "narrative_questions": [
                {
                    "question": q.question,
                    "scene_raised": q.scene_raised,
                    "scene_answered": q.scene_answered,
                    "is_answered": q.is_answered
                }
                for q in feedback.narrative_questions
            ]
        }

    def generate_analysis_summary(self, analysis_data: Dict) -> str:
        """Generate human-readable summary of analysis"""

        meta = analysis_data['metadata']
        screenplay = analysis_data['screenplay']
        feedback = analysis_data['feedback']

        summary = f"""# Analysis Summary: {meta['screenplay_title']}

## Metadata
- Saved: {meta['saved_at']}
- Reviewers: {', '.join(meta['reviewers'])}
- Scenes analyzed: {len(screenplay['scenes'])}
- Total feedback: {len(feedback)} scene reviews

## Screenplay Info
- Title: {screenplay['title']}
- Author: {screenplay.get('author', 'Unknown')}
- Scene count: {len(screenplay['scenes'])}

## Feedback Overview
{chr(10).join([
    f"- Scene {fb['scene_number']}: {fb['reviewer_name']}"
    for fb in feedback[:10]
])}
{"..." if len(feedback) > 10 else ""}

---
To load this analysis, use:
  storage.load_analysis('{meta['screenplay_slug']}')
"""

        return summary


# Example usage
if __name__ == "__main__":
    storage = AnalysisStorage()

    # List all available analyses
    print("Available screenplays:")
    for screenplay in storage.list_screenplays():
        print(f"  - {screenplay}")
        analyses = storage.list_analyses(screenplay)
        for analysis in analyses:
            print(f"    {analysis['saved_at']}: {', '.join(analysis['reviewers'])}")
