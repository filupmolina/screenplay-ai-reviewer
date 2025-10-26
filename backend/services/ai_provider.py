"""
AI Provider integration - supports multiple AI APIs

Handles requests to OpenAI, Anthropic, and other providers
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pydantic import BaseModel
import os


class AIMessage(BaseModel):
    """Standard message format across providers"""
    role: str  # system, user, assistant
    content: str


class AIResponse(BaseModel):
    """Standard response format"""
    content: str
    model: str
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None


class AIProvider(ABC):
    """Base class for AI providers"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or self._get_api_key_from_env()

    @abstractmethod
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment"""
        pass

    @abstractmethod
    def chat(self, messages: List[AIMessage], temperature: float = 0.7, max_tokens: int = 1000) -> AIResponse:
        """Send chat request to AI provider"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model being used"""
        pass


class AnthropicProvider(AIProvider):
    """Anthropic Claude API provider"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        self.model = model
        super().__init__(api_key)

    def _get_api_key_from_env(self) -> Optional[str]:
        return os.getenv("ANTHROPIC_API_KEY")

    def chat(self, messages: List[AIMessage], temperature: float = 0.7, max_tokens: int = 1000) -> AIResponse:
        """Send request to Anthropic API"""
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")

        client = anthropic.Anthropic(api_key=self.api_key)

        # Convert messages to Anthropic format
        # Extract system message if present
        system_message = None
        api_messages = []

        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        # Make request
        response = client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message,
            messages=api_messages
        )

        return AIResponse(
            content=response.content[0].text,
            model=self.model,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            cost_estimate=self._estimate_cost(response.usage.input_tokens, response.usage.output_tokens)
        )

    def _estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost based on current Anthropic pricing"""
        # Sonnet pricing (as of 2024)
        INPUT_COST_PER_1M = 3.00  # $3 per million input tokens
        OUTPUT_COST_PER_1M = 15.00  # $15 per million output tokens

        input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_1M
        output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_1M

        return input_cost + output_cost

    def get_model_name(self) -> str:
        return self.model


class OpenAIProvider(AIProvider):
    """OpenAI GPT API provider"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo-preview"):
        self.model = model
        super().__init__(api_key)

    def _get_api_key_from_env(self) -> Optional[str]:
        return os.getenv("OPENAI_API_KEY")

    def chat(self, messages: List[AIMessage], temperature: float = 0.7, max_tokens: int = 1000) -> AIResponse:
        """Send request to OpenAI API"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

        client = OpenAI(api_key=self.api_key)

        # Convert messages to OpenAI format
        api_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        # Make request
        response = client.chat.completions.create(
            model=self.model,
            messages=api_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return AIResponse(
            content=response.choices[0].message.content,
            model=self.model,
            tokens_used=response.usage.total_tokens,
            cost_estimate=self._estimate_cost(response.usage.prompt_tokens, response.usage.completion_tokens)
        )

    def _estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost based on current OpenAI pricing"""
        # GPT-4 Turbo pricing (as of 2024)
        INPUT_COST_PER_1M = 10.00  # $10 per million input tokens
        OUTPUT_COST_PER_1M = 30.00  # $30 per million output tokens

        input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_1M
        output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_1M

        return input_cost + output_cost

    def get_model_name(self) -> str:
        return self.model


class AIProviderFactory:
    """Factory for creating AI providers"""

    @staticmethod
    def create(provider_name: str, **kwargs) -> AIProvider:
        """
        Create an AI provider instance

        Args:
            provider_name: "anthropic", "openai", etc
            **kwargs: Additional arguments for provider (api_key, model, etc)

        Returns:
            AIProvider instance
        """
        providers = {
            "anthropic": AnthropicProvider,
            "openai": OpenAIProvider,
        }

        provider_class = providers.get(provider_name.lower())
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}. Available: {list(providers.keys())}")

        return provider_class(**kwargs)

    @staticmethod
    def get_available_providers() -> List[str]:
        """Get list of supported providers"""
        return ["anthropic", "openai"]
