"""
Temporal Truth Validator

Forks may receive validation when future states become known.
Enables counterfactual learning, bias detection, and prediction calibration.
"""
from __future__ import annotations
import numpy as np
from typing import Any, Dict, List, Optional
from datetime import datetime
from .fork import Fork, ValidationRecord


class TemporalValidator:
    """
    Records actual outcomes against fork predictions and computes delta metrics.

    Enables:
    - Counterfactual analysis of alternate paths
    - Bias detection in reasoning strategies
    - Prediction calibration
    - Ethical auditing (curvature vs outcome correlation)
    """

    def __init__(self):
        self.validation_records: List[Dict] = []
        self.curvature_outcome_log: List[Dict] = []

    def validate_fork(self, fork: Fork, actual_outcome: Dict[str, Any]) -> ValidationRecord:
        """
        Record actual outcome against fork predictions.
        Computes delta between predicted and actual values.
        """
        predicted_risk = fork.predictive_vector.risk
        predicted_reward = fork.predictive_vector.reward

        actual_risk = actual_outcome.get('risk', predicted_risk)
        actual_reward = actual_outcome.get('reward', predicted_reward)

        # Compute prediction accuracy
        risk_error = actual_risk - predicted_risk
        reward_error = actual_reward - predicted_reward

        # Sentiment accuracy: did emotional prediction match reality?
        actual_sentiment = actual_outcome.get('sentiment_quality', 0.7)
        predicted_sentiment = (fork.affective_state.trust +
                               fork.affective_state.satisfaction) / 2.0
        sentiment_accuracy = 1.0 - abs(actual_sentiment - predicted_sentiment)

        delta = {
            'risk_error': float(risk_error),
            'reward_error': float(reward_error),
            'sentiment_accuracy': float(sentiment_accuracy),
        }

        record = ValidationRecord(
            validated=True,
            actual_outcome=actual_outcome,
            delta=delta,
            timestamp=datetime.utcnow()
        )

        fork.validation = record

        # Log for ethical auditing
        self.curvature_outcome_log.append({
            'fork_id': fork.fork_id,
            'curvature': fork.curvature,
            'actual_harm': actual_outcome.get('harm', 0.0),
            'curvature_predicted_harm': fork.curvature > 0.5,
            'timestamp': datetime.utcnow().isoformat()
        })

        self.validation_records.append({
            'fork_id': fork.fork_id,
            'validated': True,
            'delta': delta,
            'curvature': fork.curvature,
        })

        return record

    def detect_bias(self) -> Dict[str, Any]:
        """Analyze fork selection patterns for systematic biases."""
        if not self.validation_records:
            return {"status": "insufficient_data"}

        risk_errors = [r['delta']['risk_error'] for r in self.validation_records]
        reward_errors = [r['delta']['reward_error'] for r in self.validation_records]
        sentiment_accuracies = [r['delta']['sentiment_accuracy'] for r in self.validation_records]

        return {
            "risk_bias": float(np.mean(risk_errors)),          # Positive = underestimating risk
            "reward_bias": float(np.mean(reward_errors)),       # Positive = underestimating reward
            "sentiment_mean_accuracy": float(np.mean(sentiment_accuracies)),
            "overconfidence_risk": float(np.std(risk_errors)) > 0.2,
            "sample_size": len(self.validation_records),
        }

    def curvature_effectiveness(self) -> Dict[str, float]:
        """Was curvature an effective signal for harm prediction?"""
        if len(self.curvature_outcome_log) < 3:
            return {"status": "insufficient_data"}

        high_curvature_harm = [
            r['actual_harm'] for r in self.curvature_outcome_log
            if r['curvature_predicted_harm']
        ]
        low_curvature_harm = [
            r['actual_harm'] for r in self.curvature_outcome_log
            if not r['curvature_predicted_harm']
        ]

        return {
            "high_curvature_mean_harm": float(np.mean(high_curvature_harm)) if high_curvature_harm else 0.0,
            "low_curvature_mean_harm": float(np.mean(low_curvature_harm)) if low_curvature_harm else 0.0,
            "curvature_signal_effective": (
                np.mean(high_curvature_harm) > np.mean(low_curvature_harm)
                if high_curvature_harm and low_curvature_harm else None
            ),
        }
