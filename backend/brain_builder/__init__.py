"""
Brain Builder - Build comprehensive AI reviewer personas

This module creates detailed Horror Brain personas by:
1. Deep research (interviews, analysis, expert opinions)
2. Screenplay analysis (patterns from their actual work)
3. Synthesis into nuanced, human-like persona files
"""

from .researcher import BrainResearcher
from .screenplay_analyzer import ScreenplayPatternAnalyzer
from .brain_synthesizer import BrainSynthesizer
from .brain_builder import BrainBuilder

__all__ = [
    'BrainResearcher',
    'ScreenplayPatternAnalyzer',
    'BrainSynthesizer',
    'BrainBuilder'
]
