"""
Screenplay Pattern Analyzer - Analyze director's actual screenplays

Finds patterns in:
- Structure (act breaks, pacing, scene lengths)
- Dialogue style (voice, subtext, humor)
- Character development
- Thematic execution (where themes appear, how they're woven in)
- Scene construction
- Storytelling techniques
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from models.screenplay import Screenplay
from services.parser import ScreenplayParser


@dataclass
class StructuralPatterns:
    """Patterns in screenplay structure"""
    avg_scene_length: float = 0.0
    total_scenes: int = 0
    act_break_timings: List[int] = field(default_factory=list)
    pacing_rhythm: str = ""  # "fast", "slow", "varied"
    tension_building: str = ""  # How they build tension


@dataclass
class DialoguePatterns:
    """Patterns in dialogue style"""
    avg_dialogue_length: float = 0.0
    character_voice_distinctiveness: str = ""
    subtext_usage: str = ""  # "heavy", "moderate", "minimal"
    humor_style: str = ""  # "dry", "slapstick", "dark", etc.
    naturalism_vs_stylization: str = ""


@dataclass
class CharacterPatterns:
    """Patterns in character development"""
    protagonist_traits: List[str] = field(default_factory=list)
    introduction_style: str = ""
    arc_patterns: List[str] = field(default_factory=list)
    relationship_dynamics: List[str] = field(default_factory=list)


@dataclass
class ThematicPatterns:
    """Patterns in how themes are executed"""
    core_themes: List[str] = field(default_factory=list)
    theme_frequency: Dict[str, int] = field(default_factory=dict)  # How often per scene
    integration_style: str = ""  # "subtle", "overt", "mixed"
    balance_theme_vs_entertainment: str = ""


@dataclass
class ScreenplayAnalysis:
    """Complete analysis of a director's screenplays"""
    director_name: str
    screenplays_analyzed: List[str] = field(default_factory=list)
    structural: StructuralPatterns = field(default_factory=StructuralPatterns)
    dialogue: DialoguePatterns = field(default_factory=DialoguePatterns)
    character: CharacterPatterns = field(default_factory=CharacterPatterns)
    thematic: ThematicPatterns = field(default_factory=ThematicPatterns)
    notable_techniques: List[str] = field(default_factory=list)
    genre_conventions_followed: List[str] = field(default_factory=list)
    genre_conventions_broken: List[str] = field(default_factory=list)


class ScreenplayPatternAnalyzer:
    """
    Analyzes patterns across multiple screenplays by a director

    Identifies:
    - What they do consistently
    - What they vary
    - Their signature techniques
    - How they balance different elements
    """

    def __init__(self):
        """Initialize analyzer"""
        self.parser = ScreenplayParser()

    def analyze_screenplay(
        self,
        screenplay_path: str,
        director_name: str
    ) -> ScreenplayAnalysis:
        """
        Analyze a single screenplay for patterns

        Args:
            screenplay_path: Path to screenplay PDF/Fountain file
            director_name: Director's name

        Returns:
            ScreenplayAnalysis with identified patterns
        """
        # Parse screenplay
        screenplay = self.parser.parse_file(screenplay_path)

        analysis = ScreenplayAnalysis(
            director_name=director_name,
            screenplays_analyzed=[screenplay.title or screenplay_path]
        )

        # Analyze different aspects
        analysis.structural = self._analyze_structure(screenplay)
        analysis.dialogue = self._analyze_dialogue(screenplay)
        analysis.character = self._analyze_characters(screenplay)
        analysis.thematic = self._analyze_themes(screenplay)
        analysis.notable_techniques = self._identify_techniques(screenplay)

        return analysis

    def analyze_multiple_screenplays(
        self,
        screenplay_paths: List[str],
        director_name: str
    ) -> ScreenplayAnalysis:
        """
        Analyze multiple screenplays to find consistent patterns

        Args:
            screenplay_paths: List of screenplay file paths
            director_name: Director's name

        Returns:
            Aggregated ScreenplayAnalysis
        """
        analyses = []

        for path in screenplay_paths:
            try:
                analysis = self.analyze_screenplay(path, director_name)
                analyses.append(analysis)
            except Exception as e:
                print(f"⚠️  Error analyzing {path}: {e}")
                continue

        # Aggregate patterns across all screenplays
        aggregated = self._aggregate_analyses(analyses, director_name)

        return aggregated

    def _analyze_structure(self, screenplay: Screenplay) -> StructuralPatterns:
        """Analyze structural patterns"""
        patterns = StructuralPatterns()

        if screenplay.scenes:
            patterns.total_scenes = len(screenplay.scenes)

            # Calculate average scene length
            scene_lengths = []
            for scene in screenplay.scenes:
                # Count dialogue + action lines
                length = len(scene.dialogue_blocks) + len(scene.action_blocks)
                scene_lengths.append(length)

            if scene_lengths:
                patterns.avg_scene_length = sum(scene_lengths) / len(scene_lengths)

                # Determine pacing
                variance = max(scene_lengths) - min(scene_lengths)
                if variance < 5:
                    patterns.pacing_rhythm = "consistent"
                elif variance < 15:
                    patterns.pacing_rhythm = "varied"
                else:
                    patterns.pacing_rhythm = "highly_varied"

        return patterns

    def _analyze_dialogue(self, screenplay: Screenplay) -> DialoguePatterns:
        """Analyze dialogue patterns"""
        patterns = DialoguePatterns()

        all_dialogue = []
        for scene in screenplay.scenes:
            for dialogue in scene.dialogue_blocks:
                all_dialogue.append(dialogue.text)

        if all_dialogue:
            # Average dialogue length
            avg_length = sum(len(d.split()) for d in all_dialogue) / len(all_dialogue)
            patterns.avg_dialogue_length = avg_length

            # Classify style based on length
            if avg_length < 8:
                patterns.naturalism_vs_stylization = "naturalistic (short exchanges)"
            elif avg_length < 15:
                patterns.naturalism_vs_stylization = "balanced"
            else:
                patterns.naturalism_vs_stylization = "stylized (longer speeches)"

        return patterns

    def _analyze_characters(self, screenplay: Screenplay) -> CharacterPatterns:
        """Analyze character patterns"""
        patterns = CharacterPatterns()

        # Get protagonist (most dialogue)
        if screenplay.scenes:
            character_dialogue_count = {}
            for scene in screenplay.scenes:
                for dialogue in scene.dialogue_blocks:
                    char = dialogue.character
                    character_dialogue_count[char] = character_dialogue_count.get(char, 0) + 1

            if character_dialogue_count:
                protagonist = max(character_dialogue_count, key=character_dialogue_count.get)

                # Analyze protagonist introduction (first scene they appear)
                for i, scene in enumerate(screenplay.scenes):
                    char_names = [d.character for d in scene.dialogue_blocks]
                    if protagonist in char_names:
                        if i == 0:
                            patterns.introduction_style = "immediate (scene 1)"
                        elif i < 3:
                            patterns.introduction_style = "early (first few scenes)"
                        else:
                            patterns.introduction_style = f"delayed (scene {i+1})"
                        break

        return patterns

    def _analyze_themes(self, screenplay: Screenplay) -> ThematicPatterns:
        """Analyze thematic patterns"""
        patterns = ThematicPatterns()

        # This is simplified - real implementation would use
        # NLP to identify themes

        # For now, note that this needs to be done with AI analysis
        patterns.integration_style = "needs_ai_analysis"

        return patterns

    def _identify_techniques(self, screenplay: Screenplay) -> List[str]:
        """Identify notable storytelling techniques"""
        techniques = []

        if screenplay.scenes:
            # Check for cold open
            if len(screenplay.scenes) > 0:
                first_scene = screenplay.scenes[0]
                if first_scene.heading and "EXT" in first_scene.heading:
                    techniques.append("Often opens with exterior establishing shot")

            # Check for dialogue-heavy vs action-heavy
            total_dialogue = sum(len(s.dialogue_blocks) for s in screenplay.scenes)
            total_action = sum(len(s.action_blocks) for s in screenplay.scenes)

            ratio = total_dialogue / (total_action + 1)  # Avoid division by zero
            if ratio > 2:
                techniques.append("Dialogue-driven storytelling")
            elif ratio < 0.5:
                techniques.append("Action-driven storytelling")
            else:
                techniques.append("Balanced dialogue and action")

        return techniques

    def _aggregate_analyses(
        self,
        analyses: List[ScreenplayAnalysis],
        director_name: str
    ) -> ScreenplayAnalysis:
        """Aggregate patterns across multiple screenplay analyses"""

        if not analyses:
            return ScreenplayAnalysis(director_name=director_name)

        aggregated = ScreenplayAnalysis(
            director_name=director_name,
            screenplays_analyzed=[
                title
                for analysis in analyses
                for title in analysis.screenplays_analyzed
            ]
        )

        # Aggregate structural patterns
        avg_scene_lengths = [a.structural.avg_scene_length for a in analyses if a.structural.avg_scene_length > 0]
        if avg_scene_lengths:
            aggregated.structural.avg_scene_length = sum(avg_scene_lengths) / len(avg_scene_lengths)

        # Aggregate techniques (find common ones)
        all_techniques = [tech for a in analyses for tech in a.notable_techniques]
        technique_counts = {}
        for tech in all_techniques:
            technique_counts[tech] = technique_counts.get(tech, 0) + 1

        # Keep techniques that appear in multiple screenplays
        common_techniques = [
            tech for tech, count in technique_counts.items()
            if count >= len(analyses) / 2  # Appears in at least half
        ]
        aggregated.notable_techniques = common_techniques

        return aggregated

    def generate_pattern_report(
        self,
        analysis: ScreenplayAnalysis
    ) -> str:
        """Generate human-readable pattern analysis report"""

        report = f"""# Screenplay Pattern Analysis: {analysis.director_name}

## Screenplays Analyzed
{chr(10).join(f'- {title}' for title in analysis.screenplays_analyzed)}

## Structural Patterns
- Total scenes: {analysis.structural.total_scenes}
- Average scene length: {analysis.structural.avg_scene_length:.1f} beats
- Pacing rhythm: {analysis.structural.pacing_rhythm}

## Dialogue Style
- Average dialogue length: {analysis.dialogue.avg_dialogue_length:.1f} words
- Style: {analysis.dialogue.naturalism_vs_stylization}

## Character Development
- Protagonist introduction: {analysis.character.introduction_style}

## Notable Techniques
{chr(10).join(f'- {tech}' for tech in analysis.notable_techniques)}

---
Generated by Brain Builder
"""
        return report
