"""
Square — Belief Manifold (M_KG)

Memory and knowledge. Stores facts, fork ancestry, reasoning traces,
and temporal validation records. In production: PostgreSQL + Neo4j + FAISS.
In this implementation: in-memory stores with the same interface.
"""
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime
from ..core.fork import Fork


class BeliefStore:
    """In-memory belief store. Production: PostgreSQL + pgvector."""

    def __init__(self):
        self.facts: Dict[str, Dict] = {}           # Validated beliefs
        self.fork_ancestry: Dict[str, Fork] = {}   # Complete fork history
        self.reasoning_traces: List[Dict] = []     # Step-by-step inference paths
        self.sessions: Dict[str, Dict] = {}        # Active sessions
        self._embeddings: Dict[str, List[float]] = {}  # Vector index (FAISS mock)

    def create_session(self, user_id: str = "default") -> str:
        session_id = str(uuid.uuid4())[:8]
        self.sessions[session_id] = {
            'id': session_id,
            'user_id': user_id,
            'state': 'active',
            'created_at': datetime.utcnow().isoformat(),
            'fork_count': 0,
        }
        return session_id

    def store_fact(self, key: str, value: Any, confidence: float = 1.0) -> None:
        self.facts[key] = {
            'value': value,
            'confidence': confidence,
            'timestamp': datetime.utcnow().isoformat(),
        }

    def retrieve_fact(self, key: str) -> Optional[Dict]:
        return self.facts.get(key)

    def store_fork(self, fork: Fork) -> None:
        self.fork_ancestry[fork.fork_id] = fork
        if fork.session_id in self.sessions:
            self.sessions[fork.session_id]['fork_count'] += 1

    def get_fork(self, fork_id: str) -> Optional[Fork]:
        return self.fork_ancestry.get(fork_id)

    def get_session_forks(self, session_id: str) -> List[Fork]:
        return [f for f in self.fork_ancestry.values() if f.session_id == session_id]

    def store_trace(self, fork_id: str, trace: List[str]) -> None:
        self.reasoning_traces.append({
            'fork_id': fork_id,
            'trace': trace,
            'timestamp': datetime.utcnow().isoformat(),
        })

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Mock semantic search. Production: pgvector/FAISS."""
        # Simple keyword matching as approximation
        results = []
        for key, fact in self.facts.items():
            val_str = str(fact['value']).lower()
            if any(word.lower() in val_str for word in query.split()):
                results.append({'key': key, **fact, 'similarity': 0.8})
        return results[:top_k]

    def snapshot(self, query: str) -> Dict:
        """Extract relevant knowledge snapshot for a query."""
        relevant_facts = self.semantic_search(query, top_k=3)
        return {
            'query': query,
            'facts': relevant_facts,
            'total_facts': len(self.facts),
            'timestamp': datetime.utcnow().isoformat(),
        }


class Square:
    """
    The Belief Manifold.
    Interface to memory, knowledge, and fork ancestry.
    """

    def __init__(self):
        self.store = BeliefStore()

    def new_session(self, user_id: str = "default") -> str:
        return self.store.create_session(user_id)

    def remember(self, key: str, value: Any, confidence: float = 1.0) -> None:
        self.store.store_fact(key, value, confidence)

    def recall(self, key: str) -> Optional[Any]:
        fact = self.store.retrieve_fact(key)
        return fact['value'] if fact else None

    def archive_fork(self, fork: Fork) -> None:
        self.store.store_fork(fork)
        self.store.store_trace(fork.fork_id, fork.logic_path)

    def retrieve_context(self, query: str) -> Dict:
        return self.store.snapshot(query)

    def get_fork_lineage(self, fork_id: str) -> List[Fork]:
        """Get complete ancestry chain for a fork."""
        lineage = []
        current_id = fork_id
        visited = set()
        while current_id and current_id not in visited:
            visited.add(current_id)
            fork = self.store.get_fork(current_id)
            if fork:
                lineage.append(fork)
                current_id = fork.parent_fork_id
            else:
                break
        return lineage

    def stats(self) -> Dict:
        return {
            'total_facts': len(self.store.facts),
            'total_forks': len(self.store.fork_ancestry),
            'active_sessions': len(self.store.sessions),
        }
