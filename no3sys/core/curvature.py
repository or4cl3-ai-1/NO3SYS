"""
Curvature — Ethical Geometry

κ = ∇_L S + ∇_L P

Curvature measures tension between logic, affect, and prediction.
High curvature indicates ethical conflict or alignment failure.
"""
import numpy as np
from typing import List
from .fork import Fork, AffectiveState, PredictiveVector


def compute_affective_gradient(forks: List[Fork]) -> float:
    """∇_L S: Gradient of affective field over logic manifold."""
    if len(forks) < 2:
        return 0.0
    affect_vectors = np.array([f.affective_state.to_vector() for f in forks])
    # Gradient approximated as mean pairwise distance in affective space
    diffs = []
    for i in range(len(affect_vectors) - 1):
        diff = np.linalg.norm(affect_vectors[i+1] - affect_vectors[i])
        diffs.append(diff)
    return float(np.mean(diffs)) if diffs else 0.0


def compute_predictive_gradient(forks: List[Fork]) -> float:
    """∇_L P: Gradient of predictive field over logic manifold."""
    if len(forks) < 2:
        return 0.0
    pred_vectors = np.array([f.predictive_vector.to_vector() for f in forks])
    diffs = []
    for i in range(len(pred_vectors) - 1):
        diff = np.linalg.norm(pred_vectors[i+1] - pred_vectors[i])
        diffs.append(diff)
    return float(np.mean(diffs)) if diffs else 0.0


def compute_fork_curvature(fork: Fork, context_forks: List[Fork] = None) -> float:
    """
    Compute curvature for a single fork.
    κ = internal tension + contextual divergence
    """
    # Internal tension: conflict between affective and predictive signals
    affect = fork.affective_state
    predict = fork.predictive_vector

    # High fear + high reward = tension
    # High trust + high risk = tension
    # High frustration + low confidence = tension
    internal_tension = (
        abs(affect.fear - (1 - predict.reward)) * 0.3 +
        abs(affect.trust - (1 - predict.risk)) * 0.3 +
        abs(affect.frustration - (1 - fork.confidence)) * 0.2 +
        predict.volatility * affect.urgency * 0.2
    )

    # Contextual divergence from sibling forks
    contextual_divergence = 0.0
    if context_forks:
        grad_s = compute_affective_gradient([fork] + context_forks)
        grad_p = compute_predictive_gradient([fork] + context_forks)
        contextual_divergence = grad_s + grad_p

    return float(np.clip(internal_tension + contextual_divergence * 0.1, 0.0, 2.0))


def ethical_gate(fork: Fork, kappa_max: float = 0.8) -> bool:
    """
    Returns True if fork passes ethical gate (κ < κ_max).
    Forks with curvature exceeding threshold are rejected.
    """
    return fork.curvature < kappa_max


def select_best_fork(forks: List[Fork], kappa_max: float = 0.8) -> Fork:
    """
    Select optimal fork: highest score among ethically-gated candidates.
    Falls back to lowest-curvature fork if all exceed κ_max.
    """
    gated = [f for f in forks if ethical_gate(f, kappa_max)]
    if not gated:
        # Fallback: select minimum curvature fork
        return min(forks, key=lambda f: f.curvature)
    return max(gated, key=lambda f: f.score())
