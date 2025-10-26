"""
Brain Researcher - Deep research on directors/writers

Gathers comprehensive information from:
- Interviews (video, written, podcasts)
- Expert analysis (criticism, academic papers)
- Public statements (social media, talks)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from anthropic import Anthropic
import os


@dataclass
class ResearchSource:
    """Single source of information about the director"""
    url: str
    title: str
    content: str
    source_type: str  # interview, analysis, social, commentary
    date: Optional[str] = None
    confidence: float = 1.0  # How reliable is this source


@dataclass
class ResearchFindings:
    """Aggregated research about a director"""
    director_name: str
    sources: List[ResearchSource] = field(default_factory=list)

    # Extracted knowledge
    creative_philosophy: List[str] = field(default_factory=list)
    process_insights: List[str] = field(default_factory=list)
    themes_and_interests: List[str] = field(default_factory=list)
    technical_preferences: List[str] = field(default_factory=list)
    pet_peeves: List[str] = field(default_factory=list)
    advice_given: List[str] = field(default_factory=list)
    real_quotes: List[str] = field(default_factory=list)
    influences: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'director_name': self.director_name,
            'sources': [
                {
                    'url': s.url,
                    'title': s.title,
                    'content': s.content[:500],  # Truncate for storage
                    'source_type': s.source_type,
                    'date': s.date,
                    'confidence': s.confidence
                }
                for s in self.sources
            ],
            'creative_philosophy': self.creative_philosophy,
            'process_insights': self.process_insights,
            'themes_and_interests': self.themes_and_interests,
            'technical_preferences': self.technical_preferences,
            'pet_peeves': self.pet_peeves,
            'advice_given': self.advice_given,
            'real_quotes': self.real_quotes,
            'influences': self.influences
        }


class BrainResearcher:
    """
    Conducts deep research on directors/writers

    Uses Claude to:
    1. Generate search queries
    2. Analyze gathered content
    3. Extract key insights
    4. Synthesize findings
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize researcher with Anthropic API"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-haiku-20241022"  # Fast and cost-effective

    def research_director(
        self,
        director_name: str,
        focus_areas: Optional[List[str]] = None
    ) -> ResearchFindings:
        """
        Conduct comprehensive research on a director

        Args:
            director_name: Name of director/writer
            focus_areas: Optional specific areas to focus on

        Returns:
            ResearchFindings with all gathered information
        """
        findings = ResearchFindings(director_name=director_name)

        # Phase 1: Generate research questions
        research_questions = self._generate_research_questions(
            director_name, focus_areas
        )

        # Phase 2: For each question, perform research
        # NOTE: This is a simplified version - real implementation would
        # use web search API or require manual input of sources

        print(f"\n🔍 Research Questions for {director_name}:")
        for i, question in enumerate(research_questions, 1):
            print(f"  {i}. {question}")

        print(f"\n📋 Next steps:")
        print(f"  1. Search web for answers to these questions")
        print(f"  2. Gather interviews, articles, video transcripts")
        print(f"  3. Run analyze_sources() with gathered content")

        return findings

    def _generate_research_questions(
        self,
        director_name: str,
        focus_areas: Optional[List[str]] = None
    ) -> List[str]:
        """Generate targeted research questions"""

        focus_context = ""
        if focus_areas:
            focus_context = f"\n\nFocus especially on: {', '.join(focus_areas)}"

        prompt = f"""Generate 10-15 specific research questions to deeply understand {director_name}'s creative process, philosophy, and approach to filmmaking.

Questions should cover:
- Their creative philosophy and what drives their choices
- Their process and mindset when working
- Themes and interests they care about
- Technical preferences and techniques
- What they look for in scripts
- What concerns or frustrates them
- Advice they give to other filmmakers
- Their influences and inspirations
{focus_context}

Return ONLY the questions, one per line, numbered."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse questions from response
        questions_text = response.content[0].text
        questions = [
            q.strip().lstrip('0123456789.').strip()
            for q in questions_text.split('\n')
            if q.strip() and any(c.isalpha() for c in q)
        ]

        return questions

    def analyze_sources(
        self,
        findings: ResearchFindings,
        sources: List[ResearchSource]
    ) -> ResearchFindings:
        """
        Analyze gathered sources and extract insights

        Args:
            findings: Existing research findings to update
            sources: New sources to analyze

        Returns:
            Updated ResearchFindings
        """
        findings.sources.extend(sources)

        # Analyze each source
        for source in sources:
            insights = self._extract_insights_from_source(
                findings.director_name,
                source
            )

            # Add to appropriate categories
            findings.creative_philosophy.extend(insights.get('philosophy', []))
            findings.process_insights.extend(insights.get('process', []))
            findings.themes_and_interests.extend(insights.get('themes', []))
            findings.technical_preferences.extend(insights.get('technical', []))
            findings.pet_peeves.extend(insights.get('pet_peeves', []))
            findings.advice_given.extend(insights.get('advice', []))
            findings.real_quotes.extend(insights.get('quotes', []))
            findings.influences.extend(insights.get('influences', []))

        # Deduplicate and synthesize
        findings = self._deduplicate_findings(findings)

        return findings

    def _extract_insights_from_source(
        self,
        director_name: str,
        source: ResearchSource
    ) -> Dict[str, List[str]]:
        """Extract structured insights from a single source"""

        prompt = f"""Analyze this {source.source_type} about {director_name} and extract key insights.

Source: {source.title}
Content: {source.content}

Extract and categorize:
1. Creative philosophy (what drives their choices)
2. Process insights (how they work)
3. Themes and interests (what they care about)
4. Technical preferences (techniques, tools, style)
5. Pet peeves (what frustrates them in scripts/filmmaking)
6. Advice given (tips for other filmmakers)
7. Real quotes (actual things they said, verbatim)
8. Influences (who/what inspired them)

Format as JSON:
{{
  "philosophy": ["insight 1", "insight 2"],
  "process": ["insight 1", "insight 2"],
  ...
}}

Be specific and quote directly when possible."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        import json
        try:
            insights = json.loads(response.content[0].text)
        except json.JSONDecodeError:
            # Fallback: simple parsing
            insights = {
                'philosophy': [],
                'process': [],
                'themes': [],
                'technical': [],
                'pet_peeves': [],
                'advice': [],
                'quotes': [],
                'influences': []
            }

        return insights

    def _deduplicate_findings(
        self,
        findings: ResearchFindings
    ) -> ResearchFindings:
        """Remove duplicate insights and consolidate similar ones"""

        # Simple deduplication for now
        findings.creative_philosophy = list(set(findings.creative_philosophy))
        findings.process_insights = list(set(findings.process_insights))
        findings.themes_and_interests = list(set(findings.themes_and_interests))
        findings.technical_preferences = list(set(findings.technical_preferences))
        findings.pet_peeves = list(set(findings.pet_peeves))
        findings.advice_given = list(set(findings.advice_given))
        findings.real_quotes = list(set(findings.real_quotes))
        findings.influences = list(set(findings.influences))

        return findings

    def generate_research_report(
        self,
        findings: ResearchFindings
    ) -> str:
        """Generate human-readable research report"""

        report = f"""# Research Report: {findings.director_name}

## Sources Analyzed
{len(findings.sources)} sources ({
    len([s for s in findings.sources if s.source_type == 'interview'])} interviews,
    {len([s for s in findings.sources if s.source_type == 'analysis'])} analyses,
    {len([s for s in findings.sources if s.source_type == 'commentary'])} commentaries)

## Creative Philosophy
{chr(10).join(f'- {p}' for p in findings.creative_philosophy[:10])}

## Process & Mindset
{chr(10).join(f'- {p}' for p in findings.process_insights[:10])}

## Themes & Interests
{chr(10).join(f'- {t}' for t in findings.themes_and_interests[:10])}

## Technical Preferences
{chr(10).join(f'- {t}' for t in findings.technical_preferences[:10])}

## Pet Peeves
{chr(10).join(f'- {p}' for p in findings.pet_peeves[:10])}

## Notable Quotes
{chr(10).join(f'> {q}' for q in findings.real_quotes[:10])}

## Influences
{chr(10).join(f'- {i}' for i in findings.influences[:10])}

---
Generated by Brain Builder
"""
        return report
