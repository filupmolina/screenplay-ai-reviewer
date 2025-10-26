"""
Brain Builder - Main orchestrator

Coordinates:
1. Deep research (BrainResearcher)
2. Screenplay analysis (ScreenplayPatternAnalyzer)
3. Synthesis (BrainSynthesizer)

Usage:
    builder = BrainBuilder()
    persona = builder.build_brain("Jordan Peele", screenplay_paths=[...])
"""

from typing import List, Optional
from pathlib import Path

from .researcher import BrainResearcher, ResearchSource, ResearchFindings
from .screenplay_analyzer import ScreenplayPatternAnalyzer, ScreenplayAnalysis
from .brain_synthesizer import BrainSynthesizer, BrainPersona


class BrainBuilder:
    """
    Main Brain Builder orchestrator

    Builds comprehensive Horror Brain 2.0 personas through:
    1. Deep research on director/writer
    2. Analysis of their screenplays
    3. Synthesis into nuanced persona file
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Brain Builder"""
        self.researcher = BrainResearcher(api_key=api_key)
        self.screenplay_analyzer = ScreenplayPatternAnalyzer()
        self.synthesizer = BrainSynthesizer(api_key=api_key)

    def build_brain(
        self,
        director_name: str,
        screenplay_paths: Optional[List[str]] = None,
        research_sources: Optional[List[ResearchSource]] = None,
        focus_areas: Optional[List[str]] = None,
        output_path: Optional[str] = None
    ) -> BrainPersona:
        """
        Build complete Horror Brain 2.0 persona

        Args:
            director_name: Name of director/writer
            screenplay_paths: Paths to their screenplays (optional)
            research_sources: Pre-gathered research sources (optional)
            focus_areas: Specific areas to focus on (optional)
            output_path: Where to save persona file (optional)

        Returns:
            BrainPersona with complete persona document

        Process:
            1. Generate research questions
            2. (Manual step: gather sources)
            3. Analyze research sources
            4. Analyze screenplays (if provided)
            5. Synthesize into persona
            6. Save to file (if output_path provided)
        """

        print(f"\n🧠 Building Horror Brain 2.0: {director_name}")
        print("=" * 60)

        # Phase 1: Research
        print("\n📚 Phase 1: Deep Research")
        print("-" * 60)

        research = self.researcher.research_director(
            director_name,
            focus_areas=focus_areas
        )

        if research_sources:
            print(f"\n  Analyzing {len(research_sources)} provided sources...")
            research = self.researcher.analyze_sources(research, research_sources)
            print(f"  ✓ Extracted insights from sources")
        else:
            print(f"\n  ⚠️  No sources provided yet")
            print(f"  → Gather sources manually, then run:")
            print(f"     builder.add_research_sources(research, sources)")

        # Phase 2: Screenplay Analysis
        screenplay_analysis = None
        if screenplay_paths:
            print(f"\n🎬 Phase 2: Screenplay Analysis")
            print("-" * 60)
            print(f"  Analyzing {len(screenplay_paths)} screenplays...")

            screenplay_analysis = self.screenplay_analyzer.analyze_multiple_screenplays(
                screenplay_paths,
                director_name
            )

            print(f"  ✓ Identified patterns across screenplays")
        else:
            print(f"\n  ⚠️  No screenplays provided for analysis")
            print(f"  → This is optional but highly recommended")

        # Phase 3: Synthesis
        print(f"\n🔧 Phase 3: Brain Synthesis")
        print("-" * 60)
        print(f"  Generating Horror Brain 2.0 persona...")

        persona = self.synthesizer.synthesize_brain(
            research,
            screenplay_analysis
        )

        print(f"  ✓ Synthesized comprehensive persona")
        print(f"  Confidence: {persona.confidence_score:.2%}")

        # Save if output path provided
        if output_path:
            self.synthesizer.save_persona(persona, output_path)

        print("\n" + "=" * 60)
        print(f"✅ Horror Brain 2.0 Complete: {director_name}")
        print("=" * 60)

        return persona

    def add_research_sources(
        self,
        research: ResearchFindings,
        sources: List[ResearchSource]
    ) -> ResearchFindings:
        """
        Add research sources to existing research findings

        Use this after initial research_director() call to add gathered sources
        """
        return self.researcher.analyze_sources(research, sources)

    def rebuild_existing_brain(
        self,
        old_brain_path: str,
        director_name: str,
        screenplay_paths: Optional[List[str]] = None,
        output_path: Optional[str] = None
    ) -> BrainPersona:
        """
        Rebuild an existing Horror Brain 1.0 as Horror Brain 2.0

        Args:
            old_brain_path: Path to existing brain PDF
            director_name: Director's name
            screenplay_paths: Paths to their screenplays (optional)
            output_path: Where to save new brain (optional)

        Returns:
            New BrainPersona (2.0 version)

        Note: This extracts text from old brain, uses as research source,
              then builds fresh 2.0 brain with improvements
        """

        print(f"\n🔄 Rebuilding {director_name} Brain as 2.0")
        print("=" * 60)

        # Extract text from old brain PDF
        # NOTE: Use pdf_extractor, NOT direct Read
        from services.pdf_extractor import PDFExtractor

        extractor = PDFExtractor()
        old_brain_text = extractor.extract_text(old_brain_path)

        # Create research source from old brain
        old_brain_source = ResearchSource(
            url=old_brain_path,
            title=f"{director_name} Horror Brain 1.0",
            content=old_brain_text,
            source_type="previous_brain",
            confidence=0.7  # Lower confidence - needs verification
        )

        # Build new brain using old brain as one source
        persona = self.build_brain(
            director_name=director_name,
            screenplay_paths=screenplay_paths,
            research_sources=[old_brain_source],
            output_path=output_path
        )

        return persona

    def generate_reports(
        self,
        director_name: str,
        research: ResearchFindings,
        screenplay_analysis: Optional[ScreenplayAnalysis] = None,
        output_dir: str = "."
    ) -> None:
        """
        Generate human-readable reports

        Creates:
        - research_report.md
        - screenplay_analysis_report.md (if analysis provided)
        """

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Research report
        research_report = self.researcher.generate_research_report(research)
        research_file = output_path / f"{director_name.replace(' ', '_')}_research_report.md"
        with open(research_file, 'w') as f:
            f.write(research_report)
        print(f"✓ Saved research report: {research_file}")

        # Screenplay analysis report
        if screenplay_analysis:
            analysis_report = self.screenplay_analyzer.generate_pattern_report(screenplay_analysis)
            analysis_file = output_path / f"{director_name.replace(' ', '_')}_screenplay_analysis.md"
            with open(analysis_file, 'w') as f:
                f.write(analysis_report)
            print(f"✓ Saved screenplay analysis: {analysis_file}")


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python brain_builder.py <director_name> [screenplay_paths...]")
        print("\nExample:")
        print("  python brain_builder.py 'Jordan Peele' get_out.pdf us.pdf nope.pdf")
        sys.exit(1)

    director_name = sys.argv[1]
    screenplay_paths = sys.argv[2:] if len(sys.argv) > 2 else None

    builder = BrainBuilder()

    output_path = f"horror_brains/{director_name.replace(' ', '_')}_v2.md"

    persona = builder.build_brain(
        director_name=director_name,
        screenplay_paths=screenplay_paths,
        output_path=output_path
    )

    print(f"\n🎉 New Horror Brain 2.0 ready!")
    print(f"   File: {output_path}")
    print(f"   Confidence: {persona.confidence_score:.2%}")
