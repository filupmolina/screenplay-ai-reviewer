"""
Brain Chat - Chat with individual Horror Brain personas

User can:
- Ask brain to elaborate on specific feedback
- Pitch fixes and get reactions
- Debate creative choices
- Get examples from brain's own work
- Ask "how would you fix this scene?"
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from anthropic import Anthropic
import os


@dataclass
class Message:
    """Single message in conversation"""
    role: str  # "user" or "assistant"
    content: str


@dataclass
class ChatSession:
    """Chat session with a Horror Brain"""
    brain_name: str
    brain_persona: str  # Full persona document
    coverage_context: Optional[str] = None  # Coverage report for context
    messages: List[Message] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        """Add message to conversation history"""
        self.messages.append(Message(role=role, content=content))

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation in Anthropic API format"""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]


class BrainChat:
    """
    Chat interface for Horror Brain personas

    Allows natural conversation with brains about screenplays,
    with context from coverage reports.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize chat system"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def start_chat(
        self,
        brain_name: str,
        brain_persona: str,
        coverage_context: Optional[str] = None
    ) -> ChatSession:
        """
        Start new chat session with a Horror Brain

        Args:
            brain_name: Name of the brain (e.g., "Jordan Peele")
            brain_persona: Full persona document
            coverage_context: Optional coverage report for context

        Returns:
            ChatSession
        """
        session = ChatSession(
            brain_name=brain_name,
            brain_persona=brain_persona,
            coverage_context=coverage_context
        )

        # Add system message to establish context
        system_intro = self._build_system_prompt(session)
        session.add_message("assistant", system_intro)

        return session

    def send_message(
        self,
        session: ChatSession,
        user_message: str
    ) -> str:
        """
        Send message to brain and get response

        Args:
            session: Active chat session
            user_message: User's message

        Returns:
            Brain's response
        """

        # Add user message to history
        session.add_message("user", user_message)

        # Build system prompt
        system_prompt = self._build_system_prompt(session)

        # Get conversation history (excluding system intro)
        conversation = [
            {"role": msg.role, "content": msg.content}
            for msg in session.messages[1:]  # Skip system intro
        ]

        # Call API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=conversation
        )

        # Extract response
        brain_response = response.content[0].text

        # Add to history
        session.add_message("assistant", brain_response)

        return brain_response

    def _build_system_prompt(self, session: ChatSession) -> str:
        """Build system prompt for brain conversation"""

        prompt = f"""You are {session.brain_name}, engaging in a conversation about screenplay craft.

# Your Persona

{session.brain_persona}

# Conversation Context

You are chatting with a screenwriter who has received your coverage report on their screenplay.
They may ask you to:
- Elaborate on specific feedback you gave
- Explain your reasoning
- Suggest how to fix issues
- Give examples from your own work
- Debate creative choices

# How to Respond

**Stay in character**:
- Talk like {session.brain_name} would talk
- Reference your own films and experiences
- Use your actual philosophy and approach
- Be authentic to your voice

**Be helpful and specific**:
- Give concrete examples
- Reference specific scenes from your work when relevant
- Explain the "why" behind your feedback
- Suggest specific solutions, not just problems

**Be honest but constructive**:
- Don't sugarcoat issues
- But always aim to help them improve
- Praise what works
- Show enthusiasm when they nail something

**Be flexible and nuanced**:
- Acknowledge when there are multiple valid approaches
- Don't be dogmatic about rules
- Consider the context and goals of their story
- Sometimes "breaking the rules" is the right choice

**Remember**: You're not here to make them feel good or bad - you're here to help them make the best possible screenplay.
"""

        if session.coverage_context:
            prompt += f"""

# Coverage Report Context

For reference, here's the coverage report you provided:

{session.coverage_context[:2000]}  # Truncate if too long

The writer may ask about specific notes from this report.
"""

        return prompt

    def continue_conversation(
        self,
        session: ChatSession,
        user_message: str
    ) -> str:
        """Alias for send_message (more intuitive naming)"""
        return self.send_message(session, user_message)

    def get_chat_history(self, session: ChatSession) -> str:
        """Get formatted chat history"""
        history = []
        for msg in session.messages[1:]:  # Skip system intro
            speaker = "You" if msg.role == "user" else session.brain_name
            history.append(f"{speaker}: {msg.content}")
        return "\n\n".join(history)

    def save_chat(self, session: ChatSession, output_path: str) -> None:
        """Save chat session to file"""
        content = f"""# Chat with {session.brain_name}

## Conversation

{self.get_chat_history(session)}

---
Generated by Chat with the Pros
"""
        with open(output_path, 'w') as f:
            f.write(content)

        print(f"✓ Saved chat to {output_path}")


# Example usage
if __name__ == "__main__":
    # Demo conversation
    brain_persona = """# Jordan Peele Horror Brain 2.0

## Core Philosophy
Social horror - using genre to explore uncomfortable truths about society.
Every element should serve both the horror and the commentary.

## Feedback Style
Direct but encouraging. I want to help you find the deeper meaning in your story.
"""

    coverage_context = """## Opening Scene Feedback

The opening establishes tone well, but lacks the underlying dread that hooks
the audience. Consider adding something slightly "off" that creates unease
without being obviously threatening.
"""

    chat = BrainChat()
    session = chat.start_chat(
        brain_name="Jordan Peele",
        brain_persona=brain_persona,
        coverage_context=coverage_context
    )

    # Simulate conversation
    user_msg = "Jordan, you said the opening lacks dread. Can you elaborate on what you mean?"
    response = chat.send_message(session, user_msg)

    print(f"User: {user_msg}")
    print(f"\nJordan Peele: {response}")
