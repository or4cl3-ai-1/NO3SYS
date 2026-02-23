"""
Retriever — Hybrid RAG Engine

Combines vector similarity search (FAISS) with graph traversal (Neo4j).
In-memory implementation for pure-Python use; hooks for real backends.
"""
from typing import Any, Dict, List, Optional


class HybridRetriever:
    """
    Hybrid Retrieval-Augmented Generation engine.
    Combines vector and graph search with configurable weights.
    """

    def __init__(self, vector_weight: float = 0.6, graph_weight: float = 0.4):
        self.vector_weight = vector_weight
        self.graph_weight = graph_weight
        self._index: Dict[str, Any] = {}  # In-memory vector index

    def index(self, key: str, content: str, embedding: Optional[List[float]] = None) -> None:
        """Index a document for retrieval."""
        self._index[key] = {
            'content': content,
            'embedding': embedding or [0.0] * 8,
        }

    def vector_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Vector similarity search (mock implementation)."""
        results = []
        for key, doc in self._index.items():
            # Mock relevance: keyword overlap
            overlap = sum(1 for w in query.lower().split() if w in doc['content'].lower())
            if overlap > 0:
                results.append({
                    'key': key,
                    'content': doc['content'],
                    'score': overlap / max(len(query.split()), 1),
                    'source': 'vector',
                })
        return sorted(results, key=lambda x: x['score'], reverse=True)[:top_k]

    def graph_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Graph traversal search (mock implementation)."""
        # In production: Neo4j Cypher queries
        return []

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Hybrid retrieval: combine vector and graph results."""
        vector_results = self.vector_search(query, top_k)
        graph_results = self.graph_search(query, top_k // 2)

        # Merge and deduplicate
        seen = set()
        merged = []
        for r in vector_results + graph_results:
            key = r.get('key', r.get('content', ''))
            if key not in seen:
                seen.add(key)
                merged.append(r)

        return merged[:top_k]
