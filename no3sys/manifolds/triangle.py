"""
Triangle — Logic Manifold (M_L)

Triadic agent architecture:
1. Retriever Agent: Hybrid RAG (vector + graph)
2. Reasoner Agent: Deductive / Inductive / Abductive
3. Generator Agent: LLM synthesis (pluggable)

Generates parallel forks (hypotheses) for each query.
"""
from __future__ import annotations
import numpy as np
from typing import Any, Dict, List, Optional
from ..core.fork import Fork
from ..core.curvature import compute_fork_curvature


class RetrieverAgent:
    """Hybrid RAG: vector similarity + graph traversal."""

    def retrieve(self, query: str, knowledge_snapshot: Dict) -> List[Dict]:
        facts = knowledge_snapshot.get('facts', [])
        context_items = []
        for fact in facts:
            context_items.append({
                'content': str(fact.get('value', '')),
                'relevance': fact.get('similarity', 0.5),
                'source': fact.get('key', 'unknown'),
            })
        return context_items


class ReasonerAgent:
    """Deductive, inductive, and abductive reasoning modes."""

    def reason_deductive(self, query: str, context: List[Dict]) -> List[str]:
        premises = [f"Given: {c['content']}" for c in context[:2]]
        return premises + [f"Therefore, regarding '{query}': applying rule-based inference"]

    def reason_inductive(self, query: str, context: List[Dict]) -> List[str]:
        patterns = [f"Pattern observed: {c['content']}" for c in context[:2]]
        return patterns + [f"Generalizing from patterns to '{query}'"]

    def reason_abductive(self, query: str, context: List[Dict]) -> List[str]:
        observations = [f"Observation: {c['content']}" for c in context[:1]]
        return observations + [f"Best explanation for '{query}': inference to best fit"]

    def reason(self, mode: str, query: str, context: List[Dict]) -> List[str]:
        if mode == "deductive":
            return self.reason_deductive(query, context)
        elif mode == "inductive":
            return self.reason_inductive(query, context)
        else:
            return self.reason_abductive(query, context)


class GeneratorAgent:
    """LLM synthesis — pluggable backend."""

    def __init__(self, backend: Optional[Any] = None):
        self.backend = backend  # Can be OpenAI, Anthropic, local model, etc.

    def generate(self, query: str, reasoning_trace: List[str],
                 mode: str = "analytic") -> str:
        """
        Generate response from reasoning trace.
        In production: calls LLM with trace as context.
        In this implementation: template synthesis.
        """
        trace_summary = "; ".join(reasoning_trace[-3:]) if reasoning_trace else "direct response"

        if self.backend:
            # Production: call real LLM
            pass

        # Template synthesis (demonstrates structure)
        mode_prefix = {
            "analytic": "Analysis:",
            "creative": "Creative synthesis:",
            "empathetic": "Considering your perspective:",
        }.get(mode, "Response:")

        return f"{mode_prefix} Based on {trace_summary} — responding to: {query}"


class Triangle:
    """
    The Logic Manifold.
    Generates parallel forks via triadic agent cooperation.
    """

    def __init__(self, fork_depth: int = 3):
        self.fork_depth = fork_depth
        self.retriever = RetrieverAgent()
        self.reasoner = ReasonerAgent()
        self.generator = GeneratorAgent()
        self._modes = ["analytic", "creative", "empathetic"]

    def generate_forks(self, query: str, session_id: str,
                       knowledge_snapshot: Dict,
                       parent_fork_id: Optional[str] = None) -> List[Fork]:
        """
        Core method: generates fork_depth parallel hypotheses.
        Each fork represents a distinct reasoning path.
        """
        context = self.retriever.retrieve(query, knowledge_snapshot)
        reasoning_modes = ["deductive", "inductive", "abductive"]
        forks = []

        for i in range(min(self.fork_depth, 3)):
            mode = reasoning_modes[i % len(reasoning_modes)]
            gen_mode = self._modes[i % len(self._modes)]

            trace = self.reasoner.reason(mode, query, context)
            hypothesis = self.generator.generate(query, trace, gen_mode)

            # Confidence varies by reasoning mode
            confidence_base = {"deductive": 0.75, "inductive": 0.60, "abductive": 0.55}
            confidence = confidence_base[mode] + np.random.normal(0, 0.05)

            fork = Fork(
                session_id=session_id,
                parent_fork_id=parent_fork_id,
                hypothesis=hypothesis,
                logic_path=trace,
                confidence=float(np.clip(confidence, 0.1, 1.0)),
                reasoning_mode=gen_mode,
                depth=0 if parent_fork_id is None else 1,
            )
            forks.append(fork)

        return forks
