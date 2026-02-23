"""
Reasoner — Multi-Modal Inference Engine

Supports three reasoning modes:
- Deductive: From general principles to specific conclusions
- Inductive: From specific observations to general patterns
- Abductive: Inference to best explanation
"""
from typing import Dict, List, Optional


class Reasoner:
    """
    Multi-modal reasoner supporting deductive, inductive, and abductive inference.
    In production: integrates with LLM for chain-of-thought reasoning.
    """

    def __init__(self, deductive_weight: float = 0.4,
                 inductive_weight: float = 0.35,
                 abductive_weight: float = 0.25):
        self.weights = {
            'deductive': deductive_weight,
            'inductive': inductive_weight,
            'abductive': abductive_weight,
        }

    def deductive(self, query: str, premises: List[str]) -> List[str]:
        """Apply deductive reasoning: general rules → specific conclusions."""
        trace = []
        for i, premise in enumerate(premises[:3]):
            trace.append(f"P{i+1}: {premise}")
        trace.append(f"∴ Conclusion: {query} follows from the above premises")
        return trace

    def inductive(self, query: str, observations: List[str]) -> List[str]:
        """Apply inductive reasoning: specific observations → general patterns."""
        trace = []
        for i, obs in enumerate(observations[:3]):
            trace.append(f"Obs{i+1}: {obs}")
        trace.append(f"∴ Pattern: {query} generalizes across observations")
        return trace

    def abductive(self, query: str, evidence: List[str]) -> List[str]:
        """Apply abductive reasoning: find best explanation for evidence."""
        trace = []
        if evidence:
            trace.append(f"Evidence: {evidence[0]}")
        trace.append(f"Hypothesis: {query} provides the best explanation")
        trace.append("Abductive conclusion: selecting most parsimonious explanation")
        return trace

    def reason(self, mode: str, query: str, context: List[Dict]) -> List[str]:
        """Execute reasoning in specified mode."""
        content_list = [c.get('content', '') for c in context]

        if mode == 'deductive':
            return self.deductive(query, content_list)
        elif mode == 'inductive':
            return self.inductive(query, content_list)
        else:
            return self.abductive(query, content_list)

    def ensemble_reason(self, query: str, context: List[Dict]) -> Dict[str, List[str]]:
        """Run all three modes and return ensemble traces."""
        return {
            'deductive': self.deductive(query, [c.get('content', '') for c in context]),
            'inductive': self.inductive(query, [c.get('content', '') for c in context]),
            'abductive': self.abductive(query, [c.get('content', '') for c in context]),
        }
