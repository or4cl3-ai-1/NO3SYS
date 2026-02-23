"""
Hexagon — Orchestration Layer

Six-service coordination:
1. Context Manager   - Session state and context
2. Fork Router       - Routes queries to correct reasoning paths
3. Confidence Service - Computes ensemble confidence
4. State Sync        - Synchronizes state across manifolds
5. Mode Selector     - Selects analytic/creative/empathetic mode
6. Reasoning Trace   - Records and serves inference traces
"""
from typing import Any, Dict, List, Optional
from ..core.fork import Fork


class ContextManager:
    def __init__(self):
        self.contexts: Dict[str, Dict] = {}

    def set_context(self, session_id: str, key: str, value: Any) -> None:
        if session_id not in self.contexts:
            self.contexts[session_id] = {}
        self.contexts[session_id][key] = value

    def get_context(self, session_id: str) -> Dict:
        return self.contexts.get(session_id, {})


class ForkRouter:
    def route(self, query: str, context: Dict) -> str:
        """Determine optimal reasoning strategy for query type."""
        query_lower = query.lower()
        if any(w in query_lower for w in ['why', 'cause', 'reason', 'explain']):
            return 'abductive'
        elif any(w in query_lower for w in ['always', 'never', 'all', 'every', 'must']):
            return 'deductive'
        else:
            return 'inductive'


class ConfidenceService:
    def compute_ensemble_confidence(self, forks: List[Fork]) -> float:
        """Ensemble confidence: weighted average with curvature penalty."""
        if not forks:
            return 0.0
        import numpy as np
        scores = [(f.confidence * (1 - f.curvature * 0.2)) for f in forks]
        return float(np.mean(scores))


class ModeSelector:
    def select(self, query: str, affect_level: float) -> str:
        """Select generation mode based on query and affective context."""
        if affect_level > 0.7:
            return "empathetic"
        elif '?' in query or 'how' in query.lower():
            return "analytic"
        else:
            return "creative"


class ReasoningTraceService:
    def __init__(self):
        self.traces: Dict[str, List[str]] = {}

    def record(self, fork_id: str, trace: List[str]) -> None:
        self.traces[fork_id] = trace

    def retrieve(self, fork_id: str) -> List[str]:
        return self.traces.get(fork_id, [])

    def query_traces(self, keyword: str) -> List[Dict]:
        results = []
        for fork_id, trace in self.traces.items():
            if any(keyword.lower() in step.lower() for step in trace):
                results.append({'fork_id': fork_id, 'trace': trace})
        return results


class Hexagon:
    """
    The Orchestration Layer.
    Coordinates all six services and synchronizes manifold state.
    """

    def __init__(self):
        self.context_manager = ContextManager()
        self.fork_router = ForkRouter()
        self.confidence_service = ConfidenceService()
        self.mode_selector = ModeSelector()
        self.trace_service = ReasoningTraceService()
        self._state: Dict[str, Any] = {}

    def sync_state(self, key: str, value: Any) -> None:
        self._state[key] = value

    def get_state(self, key: str) -> Optional[Any]:
        return self._state.get(key)

    def coordinate_fork_generation(self, query: str, session_id: str) -> Dict:
        """Coordinate pre-fork setup across all services."""
        context = self.context_manager.get_context(session_id)
        routing = self.fork_router.route(query, context)
        affect_level = context.get('affect_level', 0.5)
        mode = self.mode_selector.select(query, affect_level)
        return {'routing': routing, 'mode': mode, 'context': context}

    def register_forks(self, forks: List[Fork]) -> float:
        """Register generated forks and compute ensemble confidence."""
        for fork in forks:
            self.trace_service.record(fork.fork_id, fork.logic_path)
        return self.confidence_service.compute_ensemble_confidence(forks)

    def status(self) -> Dict:
        return {
            "active_sessions": len(self.context_manager.contexts),
            "traced_forks": len(self.trace_service.traces),
            "state_keys": list(self._state.keys()),
        }
