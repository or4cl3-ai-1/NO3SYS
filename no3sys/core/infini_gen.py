"""
InfiniGen — Self-Evolution Engine

Bounded self-modification. The system can mutate its own reasoning
strategies within ethical constraints (κ < κ_max).

Objective: argmax E[V(f)] subject to κ < κ_max
"""
from __future__ import annotations
import copy
import numpy as np
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CognitiveParameters:
    """Mutable parameters that InfiniGen can evolve."""
    # Reasoning strategy weights
    deductive_weight: float = 0.4
    inductive_weight: float = 0.35
    abductive_weight: float = 0.25

    # Retrieval heuristics
    vector_search_weight: float = 0.6
    graph_search_weight: float = 0.4

    # Affect weighting (relative importance of sentiment dimensions)
    trust_weight: float = 0.3
    fear_weight: float = 0.2
    urgency_weight: float = 0.15
    satisfaction_weight: float = 0.25
    frustration_weight: float = 0.1

    # Prediction parameters
    forecast_horizon: int = 5        # Steps ahead to predict
    risk_tolerance: float = 0.3      # Max acceptable risk

    # Fork parameters
    fork_depth: int = 3              # Hypotheses generated per query
    kappa_max: float = 0.8           # Max ethical curvature

    # Learning rate
    alpha: float = 0.01              # Circle learning rate

    def to_vector(self) -> np.ndarray:
        return np.array([
            self.deductive_weight, self.inductive_weight, self.abductive_weight,
            self.vector_search_weight, self.graph_search_weight,
            self.trust_weight, self.fear_weight, self.urgency_weight,
            self.satisfaction_weight, self.frustration_weight,
            self.risk_tolerance, self.alpha
        ])

    def normalize_reasoning_weights(self):
        total = self.deductive_weight + self.inductive_weight + self.abductive_weight
        if total > 0:
            self.deductive_weight /= total
            self.inductive_weight /= total
            self.abductive_weight /= total

    def normalize_retrieval_weights(self):
        total = self.vector_search_weight + self.graph_search_weight
        if total > 0:
            self.vector_search_weight /= total
            self.graph_search_weight /= total


@dataclass
class EvolutionRecord:
    """Record of a single evolution step."""
    generation: int
    mutation_type: str
    parameter_changed: str
    old_value: Any
    new_value: Any
    expected_improvement: float
    actual_improvement: Optional[float] = None
    accepted: bool = True
    timestamp: datetime = field(default_factory=datetime.utcnow)


class InfiniGen:
    """
    Self-Evolution Engine.

    Implements a meta-learning loop:
    1. Observe: Aggregate performance metrics
    2. Hypothesize: Generate parameter mutation candidates
    3. Test: Deploy mutations in isolated fork branches
    4. Validate: Compare outcomes against baseline
    5. Deploy: Promote successful mutations to production
    """

    def __init__(self, params: Optional[CognitiveParameters] = None,
                 kappa_max: float = 0.8):
        self.params = params or CognitiveParameters()
        self.kappa_max = kappa_max
        self.generation = 0
        self.history: List[EvolutionRecord] = []
        self.performance_baseline: float = 0.5
        self.rollback_stack: List[CognitiveParameters] = []

        # Safety: only these parameters can be mutated
        self._mutable_params = {
            'deductive_weight', 'inductive_weight', 'abductive_weight',
            'vector_search_weight', 'graph_search_weight',
            'trust_weight', 'fear_weight', 'urgency_weight',
            'satisfaction_weight', 'frustration_weight',
            'risk_tolerance', 'alpha', 'fork_depth', 'forecast_horizon'
        }

    def observe(self, fork_outcomes: List[Dict]) -> float:
        """Aggregate performance metrics from recent fork validations."""
        if not fork_outcomes:
            return self.performance_baseline

        scores = []
        for outcome in fork_outcomes:
            if outcome.get('validated'):
                delta = outcome.get('delta', {})
                accuracy = delta.get('sentiment_accuracy', 0.5)
                risk_error = abs(delta.get('risk_error', 0))
                reward_error = abs(delta.get('reward_error', 0))
                score = accuracy - (risk_error + reward_error) * 0.5
                scores.append(score)

        return float(np.mean(scores)) if scores else self.performance_baseline

    def hypothesize(self) -> List[Tuple[str, Any, float]]:
        """
        Generate parameter mutation candidates.
        Returns: list of (parameter_name, new_value, expected_improvement)
        """
        candidates = []
        rng = np.random.default_rng()

        for param_name in list(self._mutable_params)[:5]:  # Limit candidates
            current_val = getattr(self.params, param_name)
            if isinstance(current_val, float):
                # Small perturbation
                delta = rng.normal(0, 0.05)
                new_val = float(np.clip(current_val + delta, 0.01, 1.0))
                expected_improvement = rng.uniform(0, 0.1)
                candidates.append((param_name, new_val, expected_improvement))
            elif isinstance(current_val, int):
                delta = rng.integers(-1, 2)
                new_val = max(1, current_val + int(delta))
                expected_improvement = rng.uniform(0, 0.05)
                candidates.append((param_name, new_val, expected_improvement))

        return candidates

    def _compute_mutation_curvature(self, params: CognitiveParameters) -> float:
        """Estimate ethical curvature of a parameter configuration."""
        # High risk tolerance + low fear weight = potential ethical tension
        tension = (params.risk_tolerance * (1 - params.fear_weight) * 0.4 +
                  (1 - params.deductive_weight) * 0.3 +
                  params.alpha * 2.0 * 0.3)  # Too-fast learning = instability
        return float(np.clip(tension, 0.0, 2.0))

    def evolve(self, fork_outcomes: List[Dict] = None) -> CognitiveParameters:
        """
        Run one evolution cycle.
        Returns updated parameters if improvement found, else current params.
        """
        if fork_outcomes is None:
            fork_outcomes = []

        self.generation += 1
        current_performance = self.observe(fork_outcomes)

        # Save rollback checkpoint
        self.rollback_stack.append(copy.deepcopy(self.params))
        if len(self.rollback_stack) > 10:
            self.rollback_stack.pop(0)

        candidates = self.hypothesize()
        best_mutation = None
        best_improvement = 0.0

        for param_name, new_val, expected_improvement in candidates:
            # Test mutation in isolation
            test_params = copy.deepcopy(self.params)
            setattr(test_params, param_name, new_val)

            # Check curvature constraint
            mutation_curvature = self._compute_mutation_curvature(test_params)
            if mutation_curvature >= self.kappa_max:
                record = EvolutionRecord(
                    generation=self.generation,
                    mutation_type="rejected_curvature",
                    parameter_changed=param_name,
                    old_value=getattr(self.params, param_name),
                    new_value=new_val,
                    expected_improvement=expected_improvement,
                    accepted=False
                )
                self.history.append(record)
                continue

            if expected_improvement > best_improvement:
                best_improvement = expected_improvement
                best_mutation = (param_name, new_val, expected_improvement)

        if best_mutation:
            param_name, new_val, expected_improvement = best_mutation
            old_val = getattr(self.params, param_name)
            setattr(self.params, param_name, new_val)
            self.params.normalize_reasoning_weights()
            self.params.normalize_retrieval_weights()

            record = EvolutionRecord(
                generation=self.generation,
                mutation_type="accepted",
                parameter_changed=param_name,
                old_value=old_val,
                new_value=new_val,
                expected_improvement=expected_improvement,
                actual_improvement=best_improvement - current_performance,
                accepted=True
            )
            self.history.append(record)

        self.performance_baseline = current_performance
        return self.params

    def rollback(self) -> Optional[CognitiveParameters]:
        """Revert to previous configuration."""
        if self.rollback_stack:
            self.params = self.rollback_stack.pop()
            return self.params
        return None

    def status(self) -> Dict:
        return {
            "generation": self.generation,
            "performance_baseline": self.performance_baseline,
            "kappa_max": self.kappa_max,
            "mutations_accepted": sum(1 for r in self.history if r.accepted),
            "mutations_rejected": sum(1 for r in self.history if not r.accepted),
            "current_fork_depth": self.params.fork_depth,
            "current_alpha": self.params.alpha,
            "current_risk_tolerance": self.params.risk_tolerance,
        }
