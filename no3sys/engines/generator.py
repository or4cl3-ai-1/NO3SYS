"""
Generator — LLM Synthesis Engine (Pluggable Backend)

Supports multiple LLM backends:
- OpenAI (GPT-4, etc.)
- Anthropic (Claude)
- Local models (Ollama, etc.)
- Template synthesis (default, no API required)
"""
from typing import Any, Dict, List, Optional


class Generator:
    """
    Pluggable LLM synthesis engine.
    Generates natural language responses from reasoning traces.
    """

    def __init__(self, backend: Optional[Any] = None, backend_type: str = "template"):
        self.backend = backend
        self.backend_type = backend_type
        self._generation_count = 0

    def generate(self, query: str, reasoning_trace: List[str],
                 mode: str = "analytic",
                 cognitive_context: Optional[Dict] = None) -> str:
        """
        Generate a response from query and reasoning trace.

        Args:
            query: Original user query
            reasoning_trace: Step-by-step reasoning path
            mode: Generation mode (analytic/creative/empathetic)
            cognitive_context: Additional cognitive state context

        Returns:
            Generated response string
        """
        self._generation_count += 1

        if self.backend and self.backend_type == "openai":
            return self._generate_openai(query, reasoning_trace, mode)
        elif self.backend and self.backend_type == "anthropic":
            return self._generate_anthropic(query, reasoning_trace, mode)
        else:
            return self._generate_template(query, reasoning_trace, mode)

    def _generate_template(self, query: str, reasoning_trace: List[str],
                           mode: str) -> str:
        """Template-based synthesis (no API required)."""
        trace_summary = "; ".join(reasoning_trace[-3:]) if reasoning_trace else "direct response"

        prefixes = {
            "analytic": "Analysis:",
            "creative": "Creative synthesis:",
            "empathetic": "Considering your perspective:",
        }
        prefix = prefixes.get(mode, "Response:")

        return f"{prefix} Based on {trace_summary} — responding to: {query}"

    def _generate_openai(self, query: str, reasoning_trace: List[str],
                         mode: str) -> str:
        """OpenAI backend (requires openai package and API key)."""
        # Production implementation
        try:
            import openai
            trace_context = "\n".join(reasoning_trace)
            response = self.backend.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are reasoning in {mode} mode. Reasoning trace:\n{trace_context}"},
                    {"role": "user", "content": query}
                ]
            )
            return response.choices[0].message.content
        except Exception:
            return self._generate_template(query, reasoning_trace, mode)

    def _generate_anthropic(self, query: str, reasoning_trace: List[str],
                            mode: str) -> str:
        """Anthropic backend (requires anthropic package and API key)."""
        try:
            trace_context = "\n".join(reasoning_trace)
            message = self.backend.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": f"Reasoning trace:\n{trace_context}\n\nQuery: {query}"}
                ]
            )
            return message.content[0].text
        except Exception:
            return self._generate_template(query, reasoning_trace, mode)

    def stats(self) -> Dict:
        return {
            "backend_type": self.backend_type,
            "generation_count": self._generation_count,
            "has_backend": self.backend is not None,
        }
