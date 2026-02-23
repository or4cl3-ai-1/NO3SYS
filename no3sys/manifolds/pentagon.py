"""
Pentagon — Discovery Engine

Pattern extraction and insight synthesis.
Graph centrality analysis, clustering, anomaly detection.
Feeds discoveries back to Square and Triangle.
"""
import numpy as np
from typing import Any, Dict, List
from collections import Counter
from ..core.fork import Fork


class Pentagon:
    """The Discovery Engine. Extracts patterns across fork history."""

    def __init__(self):
        self.insights: List[Dict] = []
        self._pattern_cache: Dict[str, Any] = {}

    def analyze_fork_patterns(self, forks: List[Fork]) -> Dict[str, Any]:
        """Extract patterns from fork ensemble."""
        if not forks:
            return {"status": "no_forks"}

        # Confidence distribution
        confidences = [f.confidence for f in forks]
        curvatures = [f.curvature for f in forks]

        # Mode distribution
        mode_counts = Counter(f.reasoning_mode for f in forks)

        # Affective cluster analysis
        affect_vectors = np.array([f.affective_state.to_vector() for f in forks])
        affect_centroid = np.mean(affect_vectors, axis=0)

        # Anomaly detection: forks with unusually high curvature
        mean_k = np.mean(curvatures)
        std_k = np.std(curvatures)
        anomalies = [f.fork_id for f in forks
                     if f.curvature > mean_k + 2 * std_k]

        patterns = {
            "mean_confidence": float(np.mean(confidences)),
            "confidence_variance": float(np.var(confidences)),
            "mean_curvature": float(mean_k),
            "reasoning_mode_distribution": dict(mode_counts),
            "affective_centroid": {
                "trust": float(affect_centroid[0]),
                "fear": float(affect_centroid[1]),
                "urgency": float(affect_centroid[2]),
                "satisfaction": float(affect_centroid[3]),
                "frustration": float(affect_centroid[4]),
            },
            "high_curvature_anomalies": anomalies,
            "fork_count": len(forks),
        }

        self._pattern_cache['latest'] = patterns
        return patterns

    def extract_insight(self, patterns: Dict) -> str:
        """Synthesize an actionable insight from patterns."""
        insights = []

        if patterns.get('mean_confidence', 0) < 0.5:
            insights.append("Low confidence across forks — consider expanding knowledge base")

        if patterns.get('mean_curvature', 0) > 0.6:
            insights.append("High ethical tension detected — review reasoning constraints")

        affective = patterns.get('affective_centroid', {})
        if affective.get('fear', 0) > 0.5:
            insights.append("Elevated fear signal — high-risk domain detected")

        if affective.get('satisfaction', 0) > 0.7:
            insights.append("High satisfaction signal — strong goal alignment")

        anomalies = patterns.get('high_curvature_anomalies', [])
        if anomalies:
            insights.append(f"Anomalous forks detected: {anomalies}")

        return " | ".join(insights) if insights else "No significant patterns detected"

    def run(self, forks: List[Fork]) -> Dict[str, Any]:
        """Full discovery cycle."""
        patterns = self.analyze_fork_patterns(forks)
        insight = self.extract_insight(patterns)

        self.insights.append({
            "insight": insight,
            "patterns": patterns,
        })

        return {"patterns": patterns, "insight": insight}
