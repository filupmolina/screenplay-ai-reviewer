"""
Deep Research Importer - Import ChatGPT Deep Research results

Parses ChatGPT Deep Research reports and converts them into
ResearchFindings that Brain Builder can use.
"""

from typing import Dict, List, Optional
from anthropic import Anthropic
import os
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from researcher import ResearchFindings, ResearchSource
except ImportError:
    # Fallback for when run as script
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from brain_builder.researcher import ResearchFindings, ResearchSource


class DeepResearchImporter:
    """
    Import and parse ChatGPT Deep Research results

    Takes comprehensive research report from ChatGPT and
    structures it into ResearchFindings for Brain Builder.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize importer"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def generate_research_prompt(self, director_name: str) -> str:
        """
        Generate comprehensive deep research prompt for ChatGPT

        Args:
            director_name: Name of director/writer

        Returns:
            Formatted prompt ready to paste into ChatGPT Deep Research
        """

        prompt = f"""I need deep research on {director_name}'s filmmaking process, philosophy, and creative approach for building an AI reviewer persona.

RESEARCH FOCUS AREAS:

1. Creative Philosophy & Process
   - What drives their creative choices?
   - How do they think about storytelling?
   - What makes them passionate about a project?
   - Their approach to the craft of filmmaking

2. Themes & Interests
   - What themes do they consistently explore?
   - What subjects fascinate them?
   - How do they integrate themes into their work?
   - Balance of entertainment vs deeper meaning

3. Technical Preferences
   - Structural patterns (pacing, act breaks, scene construction)
   - Dialogue style (naturalistic vs stylized)
   - Character development approach
   - Visual storytelling techniques

4. What They Look For in Scripts
   - What excites them about a screenplay?
   - Red flags and warning signs
   - Pet peeves in scripts
   - What makes a scene work for them

5. Advice & Insights
   - Advice they give to other filmmakers
   - Common mistakes they see
   - Lessons they've learned
   - Their influences and inspirations

6. Real Quotes & Examples
   - Direct quotes about their process (verbatim)
   - Examples from their own work
   - Stories about specific creative decisions
   - Behind-the-scenes insights

PRIORITY SOURCES (find and analyze these):

1. Director's Commentary Tracks
   - Find YouTube videos or transcripts of director's commentary
   - Example search: "{director_name} director's commentary"
   - These are GOLD - hours of them explaining their choices scene-by-scene

2. In-Depth Interviews
   - Long-form interviews (30+ minutes)
   - Podcasts about filmmaking (Marc Maron, Fresh Air, The Q&A, etc.)
   - Written interviews in major publications
   - Q&A sessions, masterclasses

3. Expert Analysis
   - Video essays analyzing their work
   - Film criticism and scholarly analysis
   - Books about their filmmaking
   - Industry articles about their process

4. Social Media & Public Statements
   - Twitter/X threads about filmmaking
   - Instagram posts with insights
   - Reddit AMAs
   - Public talks and presentations

DELIVERABLES:

For each source found:
1. URL or citation
2. Key quotes (verbatim, with timestamp/page number if possible)
3. Insights extracted
4. Categorize as: commentary/interview/analysis/social

Focus on QUALITY sources where {director_name} speaks in their own words about their craft.

Aim for:
- 3+ hours of director's commentary transcripts (if available)
- 10+ substantial interviews
- 5+ expert analyses
- Real quotes from multiple sources

Generate a comprehensive research report organized by the focus areas above, with sources clearly cited.
"""

        return prompt

    def import_research_report(
        self,
        director_name: str,
        chatgpt_report: str
    ) -> ResearchFindings:
        """
        Import ChatGPT Deep Research report

        Args:
            director_name: Director's name
            chatgpt_report: Full text of ChatGPT research report

        Returns:
            ResearchFindings ready for Brain Builder
        """

        print(f"\n📥 Importing ChatGPT Deep Research for {director_name}")
        print("=" * 60)

        # Parse report with Claude
        findings = self._parse_report_with_ai(director_name, chatgpt_report)

        # Print summary
        print(f"\n✓ Import complete!")
        print(f"  Sources: {len(findings.sources)}")
        print(f"  Philosophy insights: {len(findings.creative_philosophy)}")
        print(f"  Process insights: {len(findings.process_insights)}")
        print(f"  Themes: {len(findings.themes_and_interests)}")
        print(f"  Real quotes: {len(findings.real_quotes)}")

        return findings

    def _parse_report_with_ai(
        self,
        director_name: str,
        report: str
    ) -> ResearchFindings:
        """Use Claude to parse ChatGPT research report into structured data"""

        prompt = f"""Parse this ChatGPT Deep Research report about {director_name} into structured data.

Extract:
1. All sources (with URLs if provided)
2. Creative philosophy insights
3. Process and mindset insights
4. Themes and interests
5. Technical preferences
6. Pet peeves
7. Advice given to filmmakers
8. Real quotes (verbatim, with source attribution)
9. Influences

Research Report:
{report}

Return as JSON:
{{
  "sources": [
    {{
      "url": "URL or citation",
      "title": "Source title",
      "type": "commentary/interview/analysis/social",
      "key_points": ["point 1", "point 2"]
    }}
  ],
  "creative_philosophy": ["insight 1", "insight 2", ...],
  "process_insights": ["insight 1", "insight 2", ...],
  "themes_and_interests": ["theme 1", "theme 2", ...],
  "technical_preferences": ["preference 1", "preference 2", ...],
  "pet_peeves": ["peeve 1", "peeve 2", ...],
  "advice_given": ["advice 1", "advice 2", ...],
  "real_quotes": [
    "Quote 1 - Source",
    "Quote 2 - Source"
  ],
  "influences": ["influence 1", "influence 2", ...]
}}

Be comprehensive - extract ALL insights and quotes."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        try:
            data = json.loads(response.content[0].text)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response.content[0].text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                raise ValueError("Could not parse AI response as JSON")

        # Convert to ResearchFindings
        findings = ResearchFindings(director_name=director_name)

        # Convert sources
        for source_data in data.get('sources', []):
            source = ResearchSource(
                url=source_data.get('url', ''),
                title=source_data.get('title', ''),
                content='\n'.join(source_data.get('key_points', [])),
                source_type=source_data.get('type', 'unknown')
            )
            findings.sources.append(source)

        # Add insights
        findings.creative_philosophy = data.get('creative_philosophy', [])
        findings.process_insights = data.get('process_insights', [])
        findings.themes_and_interests = data.get('themes_and_interests', [])
        findings.technical_preferences = data.get('technical_preferences', [])
        findings.pet_peeves = data.get('pet_peeves', [])
        findings.advice_given = data.get('advice_given', [])
        findings.real_quotes = data.get('real_quotes', [])
        findings.influences = data.get('influences', [])

        return findings

    def save_research_report(
        self,
        director_name: str,
        report: str,
        output_dir: str = "research_reports"
    ) -> str:
        """
        Save original ChatGPT research report

        Args:
            director_name: Director's name
            report: Full ChatGPT research report
            output_dir: Directory to save to

        Returns:
            Path to saved file
        """

        import os
        from pathlib import Path
        from datetime import datetime

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename
        slug = director_name.lower().replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{slug}_chatgpt_research_{timestamp}.md"
        filepath = output_path / filename

        # Save report
        with open(filepath, 'w') as f:
            f.write(f"# ChatGPT Deep Research: {director_name}\n\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(report)

        print(f"✓ Saved research report: {filepath}")

        return str(filepath)


# Example usage
if __name__ == "__main__":
    import sys

    importer = DeepResearchImporter()

    if len(sys.argv) < 2:
        # Generate prompt
        print("Usage: python deep_research_importer.py <director_name>")
        print("\nGenerating example prompt for Jordan Peele...\n")
        print("=" * 60)
        prompt = importer.generate_research_prompt("Jordan Peele")
        print(prompt)
        print("=" * 60)
        print("\n📋 Next steps:")
        print("1. Copy the prompt above")
        print("2. Paste into ChatGPT with Deep Research enabled")
        print("3. Save ChatGPT's report as a text file")
        print("4. Run: python deep_research_importer.py 'Jordan Peele' path/to/report.txt")
    else:
        director_name = sys.argv[1]

        if len(sys.argv) < 3:
            # Generate prompt for this director
            print(f"Generating deep research prompt for {director_name}...\n")
            print("=" * 60)
            prompt = importer.generate_research_prompt(director_name)
            print(prompt)
            print("=" * 60)
        else:
            # Import research report
            report_path = sys.argv[2]

            with open(report_path, 'r') as f:
                report = f.read()

            findings = importer.import_research_report(director_name, report)

            # Save for reference
            importer.save_research_report(director_name, report)

            print(f"\n🎉 Research imported successfully!")
            print(f"   Ready to build {director_name} Horror Brain 2.0")
