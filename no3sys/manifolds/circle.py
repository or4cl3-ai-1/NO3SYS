"""
Circle — Learning Loop

C_{t+1} = C_t + α∇V

Gradient descent over the entire cognitive architecture.
Updates sentiment weights, forecast horizons, and reasoning heuristics
through continuous feedback integration.
"""
import numpy as np
from typing import Dict, List, Optional
from ..core.fork import Fork


class Circle:
    """The Learning Loop. Continuous improvement through feedback."""

    def __init__(self, alpha: float = 0.01):
        self.alpha = alpha  # Learning rate
        self.state_vector = np.zeros(12)  # C_t
        self.iteration = 0
        self.loss_history: List[float] = []

    def value_function(self, fork: Fork) -> float:
        """V(f): Value of a fork outcome."""
        return (fork.predictive_vector.reward * 0.4 +
                fork.affective_state.satisfaction * 0.3 +
                fork.affective_state.trust * 0.2 +
                fork.confidence * 0.1 -
                fork.curvature * 0.2)

    def compute_gradient(self, forks: List[Fork]) -> np.ndarray:
        """∇V: Gradient of value function over state space."""
        if not forks:
            return np.zeros(12)

        values = [self.value_function(f) for f in forks]
        mean_value = np.mean(values)

        # Approximate gradient from fork ensemble
        grad = np.zeros(12)
        for i, fork in enumerate(forks):
            v = values[i]
            deviation = v - mean_value
            # Pack fork state into gradient signal
            state = np.array([
                fork.affective_state.trust, fork.affective_state.fear,
                fork.affective_state.urgency, fork.affective_state.satisfaction,
                fork.affective_state.frustration,
                fork.predictive_vector.risk, fork.predictive_vector.reward,
                fork.predictive_vector.volatility, fork.predictive_vector.stability,
                fork.confidence, fork.curvature, float(fork.selected)
            ])
            grad += deviation * state

        return grad / max(len(forks), 1)

    def update(self, forks: List[Fork]) -> np.ndarray:
        """
        C_{t+1} = C_t + α∇V
        One learning step from fork batch.
        """
        grad = self.compute_gradient(forks)
        self.state_vector = self.state_vector + self.alpha * grad
        self.iteration += 1

        current_loss = float(np.linalg.norm(grad))
        self.loss_history.append(current_loss)

        return self.state_vector

    def stats(self) -> Dict:
        return {
            "iteration": self.iteration,
            "alpha": self.alpha,
            "current_loss": self.loss_history[-1] if self.loss_history else 0.0,
            "state_norm": float(np.linalg.norm(self.state_vector)),
        }
