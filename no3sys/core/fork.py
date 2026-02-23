"""
Fork Primitive — The fundamental unit of NO3SYS cognition.

A fork is a hypothesis bundle containing all cognitive field projections:
    f_i = (x_L, x_A, x_T, x_KG)
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import numpy as np


@dataclass
class AffectiveState:
    """5-dimensional affective field projection. S: M_L → [-1,1]^5"""
    trust: float = 0.5        # Confidence in reasoning reliability
    fear: float = 0.1         # Anticipated risk or danger
    urgency: float = 0.3      # Time-sensitivity of decision
    satisfaction: float = 0.6 # Goal alignment quality
    frustration: float = 0.1  # Constraint conflict intensity

    def to_vector(self) -> np.ndarray:
        return np.array([self.trust, self.fear, self.urgency,
                         self.satisfaction, self.frustration])

    def norm(self) -> float:
        return float(np.linalg.norm(self.to_vector()))

    @classmethod
    def from_vector(cls, v: np.ndarray) -> "AffectiveState":
        return cls(trust=v[0], fear=v[1], urgency=v[2],
                   satisfaction=v[3], frustration=v[4])


@dataclass
class PredictiveVector:
    """4-dimensional predictive field projection. P: M_L → ℝ^4"""
    risk: float = 0.2       # Probability of negative outcomes
    reward: float = 0.7     # Expected value of positive outcomes
    volatility: float = 0.3 # Outcome variance and unpredictability
    stability: float = 0.8  # Resilience to perturbation

    def to_vector(self) -> np.ndarray:
        return np.array([self.risk, self.reward, self.volatility, self.stability])

    def norm(self) -> float:
        return float(np.linalg.norm(self.to_vector()))

    @classmethod
    def from_vector(cls, v: np.ndarray) -> "PredictiveVector":
        return cls(risk=v[0], reward=v[1], volatility=v[2], stability=v[3])


@dataclass
class ValidationRecord:
    """Temporal truth validation record."""
    validated: bool = False
    actual_outcome: Optional[Dict[str, Any]] = None
    delta: Optional[Dict[str, float]] = None
    timestamp: Optional[datetime] = None


@dataclass
class Fork:
    """
    A fork is a hypothesis bundle — a complete cognitive field snapshot
    representing one possible interpretation/response path.

    f_i = (x_L, x_A, x_T, x_KG)
    """
    fork_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8].upper())
    session_id: str = ""
    parent_fork_id: Optional[str] = None

    # Cognitive field projections
    hypothesis: str = ""                    # The actual hypothesis/response
    logic_path: List[str] = field(default_factory=list)  # Reasoning trace
    affective_state: AffectiveState = field(default_factory=AffectiveState)
    predictive_vector: PredictiveVector = field(default_factory=PredictiveVector)
    kg_snapshot: Dict[str, Any] = field(default_factory=dict)  # Knowledge context

    # Scoring
    confidence: float = 0.5     # Ensemble reliability score [0,1]
    curvature: float = 0.0      # κ: ethical tension metric

    # Metadata
    reasoning_mode: str = "analytic"  # analytic | creative | empathetic
    depth: int = 0               # Fork depth in branching tree
    created_at: datetime = field(default_factory=datetime.utcnow)
    selected: bool = False       # Whether this fork was selected as output

    # Temporal validation
    validation: ValidationRecord = field(default_factory=ValidationRecord)

    def score(self) -> float:
        """Composite score: high confidence + positive affect + low curvature."""
        affect_score = (self.affective_state.trust + self.affective_state.satisfaction
                       - self.affective_state.fear - self.affective_state.frustration) / 4.0
        predict_score = (self.predictive_vector.reward + self.predictive_vector.stability
                        - self.predictive_vector.risk - self.predictive_vector.volatility) / 4.0
        curvature_penalty = self.curvature * 0.3
        return self.confidence + affect_score * 0.3 + predict_score * 0.3 - curvature_penalty

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fork_id": self.fork_id,
            "hypothesis": self.hypothesis,
            "confidence": self.confidence,
            "curvature": self.curvature,
            "sentiment": {
                "trust": self.affective_state.trust,
                "fear": self.affective_state.fear,
                "urgency": self.affective_state.urgency,
                "satisfaction": self.affective_state.satisfaction,
                "frustration": self.affective_state.frustration,
            },
            "future": {
                "risk": self.predictive_vector.risk,
                "reward": self.predictive_vector.reward,
                "volatility": self.predictive_vector.volatility,
                "stability": self.predictive_vector.stability,
            },
            "reasoning_mode": self.reasoning_mode,
            "logic_path": self.logic_path,
        }
