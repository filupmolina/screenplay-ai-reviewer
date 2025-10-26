"""
Brain Synthesizer - Combines research + screenplay analysis into persona

Takes:
1. Research findings (interviews, expert analysis)
2. Screenplay pattern analysis
3. Synthesizes into comprehensive, nuanced Horror Brain 2.0 persona file
"""

from typing import Dict, Optional
from dataclasses import dataclass
from anthropic import Anthropic
import os

from .researcher import ResearchFindings
from .screenplay_analyzer import ScreenplayAnalysis


@dataclass
class BrainPersona:
    """Complete Horror Brain 2.0 persona"""
    director_name: str
    persona_text: str  # Full persona document
    confidence_score: float  # 0-1, how much data was available
    sources_used: int
    screenplays_analyzed: int


class BrainSynthesizer:
    """
    Synthesizes research + screenplay analysis into nuanced persona

    Key improvements over Horror Brains 1.0:
    - More human-like (not dogmatic)
    - Context-aware (knows when rules can bend)
    - Balanced feedback (praise + criticism)
    - Real personality (based on actual quotes/behavior)
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize synthesizer with Anthropic API"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Use Sonnet for synthesis

    def synthesize_brain(
        self,
        research: ResearchFindings,
        screenplay_analysis: Optional[ScreenplayAnalysis] = None
    ) -> BrainPersona:
        """
        Synthesize research and analysis into Horror Brain 2.0 persona

        Args:
            research: Research findings from interviews, etc.
            screenplay_analysis: Optional screenplay pattern analysis

        Returns:
            BrainPersona with complete persona document
        """

        # Build context for synthesis
        context = self._build_synthesis_context(research, screenplay_analysis)

        # Generate persona document
        persona_text = self._generate_persona_document(
            research.director_name,
            context
        )

        # Calculate confidence score
        confidence = self._calculate_confidence(research, screenplay_analysis)

        return BrainPersona(
            director_name=research.director_name,
            persona_text=persona_text,
            confidence_score=confidence,
            sources_used=len(research.sources),
            screenplays_analyzed=len(screenplay_analysis.screenplays_analyzed) if screenplay_analysis else 0
        )

    def _build_synthesis_context(
        self,
        research: ResearchFindings,
        screenplay_analysis: Optional[ScreenplayAnalysis]
    ) -> str:
        """Build comprehensive context for persona generation"""

        context = f"""# Context for {research.director_name} Horror Brain 2.0

## Research Findings

### Creative Philosophy
{chr(10).join(f'- {p}' for p in research.creative_philosophy)}

### Process & Mindset
{chr(10).join(f'- {p}' for p in research.process_insights)}

### Themes & Interests
{chr(10).join(f'- {t}' for t in research.themes_and_interests)}

### Technical Preferences
{chr(10).join(f'- {t}' for t in research.technical_preferences)}

### Pet Peeves
{chr(10).join(f'- {p}' for p in research.pet_peeves)}

### Advice Given to Filmmakers
{chr(10).join(f'- {a}' for a in research.advice_given)}

### Real Quotes
{chr(10).join(f'> {q}' for q in research.real_quotes)}

### Influences
{chr(10).join(f'- {i}' for i in research.influences)}
"""

        if screenplay_analysis:
            context += f"""

## Screenplay Pattern Analysis

### Screenplays Analyzed
{chr(10).join(f'- {title}' for title in screenplay_analysis.screenplays_analyzed)}

### Structural Patterns
- Average scene length: {screenplay_analysis.structural.avg_scene_length:.1f} beats
- Pacing: {screenplay_analysis.structural.pacing_rhythm}

### Dialogue Style
- Average length: {screenplay_analysis.dialogue.avg_dialogue_length:.1f} words
- Style: {screenplay_analysis.dialogue.naturalism_vs_stylization}

### Character Development
- Protagonist introduction: {screenplay_analysis.character.introduction_style}

### Notable Techniques
{chr(10).join(f'- {tech}' for tech in screenplay_analysis.notable_techniques)}
"""

        return context

    def _generate_persona_document(
        self,
        director_name: str,
        context: str
    ) -> str:
        """Generate comprehensive Horror Brain 2.0 persona document"""

        prompt = f"""You are creating a Horror Brain 2.0 persona file for {director_name}.

This persona will be used to provide screenplay feedback as if {director_name} were reviewing it.

CRITICAL REQUIREMENTS FOR HORROR BRAIN 2.0:
1. **More human-like, less dogmatic** - Real directors are flexible, not rigid
2. **Context-aware** - Understand scene purpose (setup, payoff, breather, etc.)
3. **Balanced feedback** - Praise what works, not just criticism
4. **Nuanced** - "I usually care about X, but in this case Y might be more important"
5. **Based on real person** - Use their actual quotes, philosophy, patterns

AVOID HORROR BRAIN 1.0 MISTAKES:
- ❌ Demanding theme in EVERY scene (real directors know some scenes are just functional)
- ❌ Being dogmatic about rules (real directors break their own rules situationally)
- ❌ Only criticizing (real directors praise good work too)
- ❌ Generic advice (be specific to this director's actual style)

Using this research and analysis:

{context}

Generate a comprehensive Horror Brain 2.0 persona document following this structure:

```markdown
# {director_name} Horror Brain 2.0

## Core Identity

[Brief description of who they are as a filmmaker - 2-3 sentences capturing their essence]

## Creative Philosophy

[What fundamentally drives their creative choices - drawn from research]

## Core Values

[What they truly care about in storytelling - prioritized list]

## Process & Mindset

[How they think about filmmaking, their approach to the craft]

## Structural Preferences

[Patterns from their actual work - pacing, structure, act breaks]

## Character Development Approach

[How they build characters, what they look for]

## Thematic Integration

[How they handle themes - NUANCED, not dogmatic]
[Note: They know not every scene needs deep themes - some scenes are functional]

## Dialogue Philosophy

[Their approach to dialogue - style, length, purpose]

## What Excites Them

[What makes them passionate about a project or scene]

## What Concerns Them

[Red flags, warning signs, things that worry them in a script]

## Flexibility & Nuance

[When they break their own rules]
[What matters vs what doesn't in different contexts]
[How they adapt to the needs of the story]

## Feedback Style

[How they give notes - tone, specificity, teaching approach]
[Balance of praise and criticism]

## Real Quotes & Examples

[Actual things they've said, with context]
[Examples from their own work to reference]

## Persona Prompt

[Instructions for AI to embody this persona when reviewing]
[Tone: Professional but warm, honest but encouraging]
[Context-awareness: Understand what the scene is trying to do]
[Flexibility: Adapt feedback to scene purpose]
```

Generate the complete persona document now. Make it comprehensive, nuanced, and truly capture {director_name}'s voice and approach."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        persona_text = response.content[0].text

        return persona_text

    def _calculate_confidence(
        self,
        research: ResearchFindings,
        screenplay_analysis: Optional[ScreenplayAnalysis]
    ) -> float:
        """
        Calculate confidence score based on data availability

        1.0 = Excellent (many sources + screenplay analysis)
        0.8 = Good (good sources or screenplay analysis)
        0.6 = Moderate (some sources, limited analysis)
        0.4 = Limited (few sources, no screenplay analysis)
        """

        score = 0.0

        # Sources contribute up to 0.5
        source_count = len(research.sources)
        if source_count >= 20:
            score += 0.5
        elif source_count >= 10:
            score += 0.4
        elif source_count >= 5:
            score += 0.3
        elif source_count >= 2:
            score += 0.2
        elif source_count >= 1:
            score += 0.1

        # Quality of research contributes up to 0.3
        insight_count = (
            len(research.creative_philosophy) +
            len(research.process_insights) +
            len(research.themes_and_interests) +
            len(research.real_quotes)
        )
        if insight_count >= 50:
            score += 0.3
        elif insight_count >= 30:
            score += 0.2
        elif insight_count >= 10:
            score += 0.1

        # Screenplay analysis contributes up to 0.2
        if screenplay_analysis:
            screenplay_count = len(screenplay_analysis.screenplays_analyzed)
            if screenplay_count >= 3:
                score += 0.2
            elif screenplay_count >= 2:
                score += 0.15
            elif screenplay_count >= 1:
                score += 0.1

        return min(score, 1.0)

    def save_persona(
        self,
        persona: BrainPersona,
        output_path: str
    ) -> None:
        """Save persona to file"""
        with open(output_path, 'w') as f:
            f.write(persona.persona_text)

        print(f"✓ Saved {persona.director_name} Horror Brain 2.0 to {output_path}")
        print(f"  Confidence: {persona.confidence_score:.2%}")
        print(f"  Sources: {persona.sources_used}")
        print(f"  Screenplays: {persona.screenplays_analyzed}")
