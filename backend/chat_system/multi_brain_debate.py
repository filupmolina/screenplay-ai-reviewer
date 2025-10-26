"""
Multi-Brain Debate System

Allows multiple Horror Brains to:
1. Discuss screenplay issues together
2. Debate creative choices
3. "Go to another room" (debate privately, report back)
4. Reach conclusions focused on best product outcome
5. Disagree honestly (no compromise just to get along)
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from anthropic import Anthropic
import os


@dataclass
class DebateParticipant:
    """Horror Brain participating in debate"""
    name: str
    persona: str  # Full persona document


@dataclass
class DebateMessage:
    """Single message in debate"""
    speaker: str  # Brain name or "Moderator"
    content: str
    is_private: bool = False  # Private debate (brains only)


@dataclass
class DebateSession:
    """Multi-brain debate session"""
    topic: str
    participants: List[DebateParticipant]
    context: Optional[str] = None  # Scene/screenplay context
    messages: List[DebateMessage] = field(default_factory=list)
    user_visible: bool = True  # Is user watching?

    def add_message(self, speaker: str, content: str, is_private: bool = False) -> None:
        """Add message to debate"""
        self.messages.append(
            DebateMessage(speaker=speaker, content=content, is_private=is_private)
        )

    def get_public_messages(self) -> List[DebateMessage]:
        """Get only public messages (user can see)"""
        return [msg for msg in self.messages if not msg.is_private]

    def get_all_messages(self) -> List[DebateMessage]:
        """Get all messages including private debate"""
        return self.messages


class MultiBrainDebate:
    """
    Multi-brain debate system

    Facilitates conversations between multiple Horror Brains
    with goal of reaching best creative outcome.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize debate system"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def start_debate(
        self,
        topic: str,
        participants: List[DebateParticipant],
        context: Optional[str] = None,
        private_mode: bool = False
    ) -> DebateSession:
        """
        Start a new debate between Horror Brains

        Args:
            topic: What they're debating
            participants: List of Horror Brains participating
            context: Optional scene/screenplay context
            private_mode: Start in private mode (brains only)

        Returns:
            DebateSession
        """
        session = DebateSession(
            topic=topic,
            participants=participants,
            context=context,
            user_visible=not private_mode
        )

        return session

    def facilitate_debate(
        self,
        session: DebateSession,
        rounds: int = 3
    ) -> DebateSession:
        """
        Facilitate a debate for specified rounds

        Args:
            session: Active debate session
            rounds: Number of back-and-forth rounds

        Returns:
            Updated session with debate messages
        """

        for round_num in range(rounds):
            # Each participant speaks
            for participant in session.participants:
                response = self._get_brain_response(session, participant)
                session.add_message(
                    speaker=participant.name,
                    content=response,
                    is_private=not session.user_visible
                )

        return session

    def private_debate_then_report(
        self,
        session: DebateSession,
        rounds: int = 3
    ) -> str:
        """
        Brains debate privately, then report back to user

        Args:
            session: Debate session
            rounds: Number of private discussion rounds

        Returns:
            Summary report for user
        """

        # Switch to private mode
        session.user_visible = False

        # Facilitate private debate
        session = self.facilitate_debate(session, rounds=rounds)

        # Generate summary report
        report = self._generate_consensus_report(session)

        # Add report as public message
        session.user_visible = True
        session.add_message(
            speaker="Consensus",
            content=report,
            is_private=False
        )

        return report

    def _get_brain_response(
        self,
        session: DebateSession,
        participant: DebateParticipant
    ) -> str:
        """Get response from a specific brain in debate"""

        # Build conversation history
        conversation_context = self._build_conversation_context(session)

        # Build system prompt
        system_prompt = self._build_debate_system_prompt(session, participant)

        # Call API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": conversation_context}]
        )

        return response.content[0].text

    def _build_debate_system_prompt(
        self,
        session: DebateSession,
        participant: DebateParticipant
    ) -> str:
        """Build system prompt for debate participant"""

        other_participants = [p.name for p in session.participants if p.name != participant.name]

        prompt = f"""You are {participant.name}, participating in a creative debate with {', '.join(other_participants)}.

# Your Persona

{participant.persona}

# Debate Topic

{session.topic}

# Debate Context

{"User is watching this conversation." if session.user_visible else "This is a PRIVATE debate between you and the other directors. The user will see a summary later."}

# How to Engage

**Be yourself**:
- Talk like {participant.name} would talk
- Use your philosophy and approach
- Reference your own work when relevant
- Stay authentic to your voice

**Be honest and direct**:
- Say what you really think
- Don't hold back to be polite
- Disagree when you disagree
- This is about finding the BEST solution, not making everyone happy

**Be constructive**:
- Focus on the work, not egos
- Explain your reasoning
- Suggest specific solutions
- Build on others' ideas when they're good

**Be open to being wrong**:
- Consider other perspectives
- Acknowledge when someone makes a good point
- Change your mind if convinced
- It's okay to say "You're right, I didn't think of that"

**Goal**: Find the best possible creative solution
- Not compromise
- Not "everyone gets something"
- The BEST outcome for the screenplay
- Even if one person's approach wins completely

**Remember**: The user hired you all for your honest expertise. Give it to them.
"""

        return prompt

    def _build_conversation_context(self, session: DebateSession) -> str:
        """Build conversation context for next response"""

        context = f"""# Debate Topic
{session.topic}

"""

        if session.context:
            context += f"""# Screenplay Context
{session.context}

"""

        if session.messages:
            context += """# Conversation So Far

"""
            for msg in session.messages:
                context += f"{msg.speaker}: {msg.content}\n\n"

            context += """Your turn. What's your take?"""
        else:
            context += """You're speaking first. What's your take on this?"""

        return context

    def _generate_consensus_report(self, session: DebateSession) -> str:
        """Generate consensus report from private debate"""

        # Get all private messages
        debate_history = "\n\n".join([
            f"{msg.speaker}: {msg.content}"
            for msg in session.messages
            if msg.is_private
        ])

        prompt = f"""Review this private debate between {', '.join([p.name for p in session.participants])} and generate a consensus report for the user.

# Debate Topic
{session.topic}

# Private Debate
{debate_history}

# Generate Report

Create a clear, actionable report that:
1. Summarizes what they discussed
2. Shows where they agreed (these points are probably critical)
3. Shows where they disagreed (these are creative choice areas)
4. Provides their recommended solution
5. Explains the tradeoffs if relevant

Format:
```
# Consensus Report: {session.topic}

## What We Discussed
[Brief summary]

## Where We Agreed
- [Point 1]
- [Point 2]

## Where We Disagreed
- [Point 1]: [Brief description of different views]
- [Point 2]: [Brief description of different views]

## Our Recommendation
[Clear, specific recommendation]

[Reasoning and tradeoffs]

## Next Steps
[What the writer should do]

---
{', '.join([p.name for p in session.participants])}
```

Generate the report now."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def get_debate_transcript(
        self,
        session: DebateSession,
        include_private: bool = False
    ) -> str:
        """Get formatted debate transcript"""

        messages = session.get_all_messages() if include_private else session.get_public_messages()

        transcript = f"""# Debate: {session.topic}

## Participants
{', '.join([p.name for p in session.participants])}

## Conversation

"""
        for msg in messages:
            private_marker = " [PRIVATE]" if msg.is_private else ""
            transcript += f"**{msg.speaker}**{private_marker}:\n{msg.content}\n\n---\n\n"

        return transcript

    def save_debate(
        self,
        session: DebateSession,
        output_path: str,
        include_private: bool = True
    ) -> None:
        """Save debate transcript to file"""

        transcript = self.get_debate_transcript(session, include_private=include_private)

        with open(output_path, 'w') as f:
            f.write(transcript)

        print(f"✓ Saved debate transcript to {output_path}")


# Example usage
if __name__ == "__main__":
    # Demo debate
    jordan = DebateParticipant(
        name="Jordan Peele",
        persona="Social horror director focused on commentary and subtext."
    )

    sam = DebateParticipant(
        name="Sam Raimi",
        persona="Horror master who loves chaos, energy, and visceral scares."
    )

    debate = MultiBrainDebate()

    session = debate.start_debate(
        topic="Horror scene: too much or too little?",
        participants=[jordan, sam],
        context="Opening scene: Protagonist arrives at isolated house, weird neighbor interaction",
        private_mode=True
    )

    # Private debate, then report
    report = debate.private_debate_then_report(session, rounds=2)

    print("=" * 60)
    print("CONSENSUS REPORT")
    print("=" * 60)
    print(report)
