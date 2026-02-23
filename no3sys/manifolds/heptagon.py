"""
Heptagon — Affective-Predictive Manifold

Dual field architecture:
- Affective Field S: M_L → [-1,1]^5  (trust, fear, urgency, satisfaction, frustration)
- Predictive Field P: M_L → ℝ^4      (risk, reward, volatility, stability)

Curvature κ = ∇_L S + ∇_L P
"""
import numpy as np
from typing import Dict, List, Optional
from ..core.fork import Fork, AffectiveState, PredictiveVector


class Heptagon:
    """
    The Affective-Predictive Manifold.
    Scores reasoning paths along emotional and predictive dimensions.
    """

    def __init__(self):
        # Calibration weights (evolved by InfiniGen)
        self.affect_weights = np.array([0.3, 0.2, 0.15, 0.25, 0.1])
        self.predict_weights = np.array([0.25, 0.35, 0.2, 0.2])
        self._calibration_history: List[Dict] = []

    def score_affective(self, context: str, reasoning_trace: List[str]) -> AffectiveState:
        """
        Project a reasoning path to affective space.
        In production: uses trained affect classifier.
        In this implementation: heuristic scoring from text signals.
        """
        text = " ".join(reasoning_trace + [context]).lower()

        # Heuristic signal extraction
        trust = 0.5
        fear = 0.1
        urgency = 0.3
        satisfaction = 0.5
        frustration = 0.1

        # Trust signals
        trust_signals = ['confident', 'certain', 'verified', 'proven', 'reliable']
        distrust_signals = ['uncertain', 'unclear', 'ambiguous', 'unknown', 'doubt']
        trust += sum(0.08 for s in trust_signals if s in text)
        trust -= sum(0.08 for s in distrust_signals if s in text)

        # Fear/risk signals
        fear_signals = ['risk', 'danger', 'harm', 'threat', 'unsafe', 'critical']
        fear += sum(0.1 for s in fear_signals if s in text)

        # Urgency signals
        urgency_signals = ['urgent', 'immediate', 'now', 'deadline', 'critical', 'asap']
        urgency += sum(0.1 for s in urgency_signals if s in text)

        # Satisfaction signals
        satisfaction_signals = ['good', 'great', 'excellent', 'solve', 'achieve', 'success']
        satisfaction += sum(0.07 for s in satisfaction_signals if s in text)

        # Clip all to valid range
        return AffectiveState(
            trust=float(np.clip(trust, 0.0, 1.0)),
            fear=float(np.clip(fear, 0.0, 1.0)),
            urgency=float(np.clip(urgency, 0.0, 1.0)),
            satisfaction=float(np.clip(satisfaction, 0.0, 1.0)),
            frustration=float(np.clip(frustration, 0.0, 1.0)),
        )

    def score_predictive(self, hypothesis: str, reasoning_trace: List[str],
                         affective_state: AffectiveState) -> PredictiveVector:
        """
        Project a reasoning path to predictive space.
        Estimates future trajectory across risk, reward, volatility, stability.
        """
        text = " ".join(reasoning_trace + [hypothesis]).lower()

        # Base estimates
        risk = affective_state.fear * 0.5
        reward = affective_state.satisfaction * 0.6
        volatility = affective_state.urgency * 0.4
        stability = affective_state.trust * 0.7

        # Adjust from reasoning content
        risk_signals = ['fail', 'error', 'wrong', 'broken', 'crash', 'loss']
        risk += sum(0.08 for s in risk_signals if s in text)

        reward_signals = ['improve', 'benefit', 'gain', 'efficient', 'effective']
        reward += sum(0.07 for s in reward_signals if s in text)

        volatile_signals = ['change', 'dynamic', 'complex', 'vary', 'unstable']
        volatility += sum(0.06 for s in volatile_signals if s in text)

        stable_signals = ['stable', 'consistent', 'reliable', 'robust', 'steady']
        stability += sum(0.07 for s in stable_signals if s in text)

        return PredictiveVector(
            risk=float(np.clip(risk, 0.0, 1.0)),
            reward=float(np.clip(reward, 0.0, 1.0)),
            volatility=float(np.clip(volatility, 0.0, 1.0)),
            stability=float(np.clip(stability, 0.0, 1.0)),
        )

    def annotate_fork(self, fork: Fork, context: str = "") -> Fork:
        """Full affective-predictive annotation of a fork."""
        fork.affective_state = self.score_affective(context, fork.logic_path)
        fork.predictive_vector = self.score_predictive(
            fork.hypothesis, fork.logic_path, fork.affective_state
        )
        return fork

    def calibrate(self, validation_deltas: List[Dict]) -> None:
        """Update scoring weights based on temporal validation feedback."""
        if not validation_deltas:
            return

        # Adjust weights based on prediction errors
        risk_errors = np.array([d.get('risk_error', 0) for d in validation_deltas])
        reward_errors = np.array([d.get('reward_error', 0) for d in validation_deltas])

        # Simple gradient: if we systematically over/underestimate, adjust
        mean_risk_error = float(np.mean(risk_errors))
        mean_reward_error = float(np.mean(reward_errors))

        # Adjust predict weights
        self.predict_weights[0] = float(np.clip(
            self.predict_weights[0] - 0.01 * mean_risk_error, 0.1, 0.5
        ))
        self.predict_weights[1] = float(np.clip(
            self.predict_weights[1] - 0.01 * mean_reward_error, 0.1, 0.5
        ))

        self._calibration_history.append({
            'risk_error': mean_risk_error,
            'reward_error': mean_reward_error,
        })
