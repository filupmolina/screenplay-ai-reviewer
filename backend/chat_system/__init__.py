"""
Chat with the Pros - Interactive brain conversations

Allows users to:
1. Chat with individual Horror Brain personas
2. Ask for elaboration on feedback
3. Debate creative choices
4. Get examples from their work
5. Pitch fixes and get reactions
"""

from .brain_chat import BrainChat
from .multi_brain_debate import MultiBrainDebate

__all__ = ['BrainChat', 'MultiBrainDebate']
