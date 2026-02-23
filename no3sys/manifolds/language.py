"""
Language — Dual Role Architecture

π_NLU: Σ* → Ĉ  (project natural language to cognitive space)
π_NLG: Ĉ → Σ*  (project cognitive state to natural language)

Language is a coordinate chart over cognition, not cognition itself.
This separation prevents linguistic distortion of logical content.
"""
from typing import Any, Dict, List, Optional
from ..core.fork import Fork


class CognitiveState:
    """Ĉ: Internal cognitive representation, language-independent."""

    def __init__(self, intent: str, entities: List[str],
                 semantic_vector: List[float], mode: str = "analytic"):
        self.intent = intent
        self.entities = entities
        self.semantic_vector = semantic_vector
        self.mode = mode

    def to_dict(self) -> Dict:
        return {
            'intent': self.intent,
            'entities': self.entities,
            'mode': self.mode,
        }


class Language:
    """
    The Projection Layer.
    NLU projects language → cognitive space.
    NLG projects cognitive state → language.
    """

    def __init__(self):
        self._nlu_cache: Dict[str, CognitiveState] = {}

    def project_in(self, text: str) -> CognitiveState:
        """
        π_NLU: Σ* → Ĉ
        Project natural language string to cognitive representation.
        In production: uses NLU model (BERT, etc.)
        """
        if text in self._nlu_cache:
            return self._nlu_cache[text]

        # Heuristic NLU
        text_lower = text.lower()

        # Intent detection
        if any(w in text_lower for w in ['what', 'who', 'when', 'where']):
            intent = 'information_retrieval'
        elif any(w in text_lower for w in ['how', 'explain', 'describe']):
            intent = 'explanation'
        elif any(w in text_lower for w in ['should', 'recommend', 'best']):
            intent = 'recommendation'
        elif any(w in text_lower for w in ['create', 'generate', 'write', 'build']):
            intent = 'generation'
        else:
            intent = 'general_query'

        # Entity extraction (simplified)
        words = text.split()
        entities = [w for w in words if w[0].isupper() and len(w) > 2]

        # Mode from intent
        mode_map = {
            'information_retrieval': 'analytic',
            'explanation': 'analytic',
            'recommendation': 'empathetic',
            'generation': 'creative',
            'general_query': 'analytic',
        }

        state = CognitiveState(
            intent=intent,
            entities=entities,
            semantic_vector=[0.0] * 8,  # Production: embedding model
            mode=mode_map.get(intent, 'analytic'),
        )

        self._nlu_cache[text] = state
        return state

    def project_out(self, fork: Fork, cognitive_state: CognitiveState) -> str:
        """
        π_NLG: Ĉ → Σ*
        Project cognitive state (via selected fork) to natural language.
        In production: calls LLM with full cognitive context.
        """
        # In this implementation: return the fork's generated hypothesis
        # Production: this would involve a full LLM call with trace context
        return fork.hypothesis

    def serialize_cognitive_state(self, forks: List[Fork]) -> Dict:
        """Serialize cognitive state for transport or persistence."""
        return {
            "fork_count": len(forks),
            "selected_fork": next((f.fork_id for f in forks if f.selected), None),
            "ensemble_confidence": sum(f.confidence for f in forks) / max(len(forks), 1),
            "forks": [f.to_dict() for f in forks],
        }
