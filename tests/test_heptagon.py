import pytest
from no3sys.manifolds.heptagon import Heptagon
from no3sys.core.fork import Fork


def test_heptagon_annotates_fork():
    h = Heptagon()
    f = Fork(hypothesis="This is a reliable solution", logic_path=["Step 1: analyze", "Step 2: verify"])
    h.annotate_fork(f, context="risk assessment")
    assert 0.0 <= f.affective_state.trust <= 1.0
    assert 0.0 <= f.predictive_vector.risk <= 1.0


def test_heptagon_fear_signal():
    h = Heptagon()
    f = Fork(hypothesis="High risk dangerous situation", logic_path=["Risk analysis: danger detected"])
    h.annotate_fork(f, context="critical risk assessment")
    assert f.affective_state.fear > 0.1


def test_heptagon_calibrate():
    h = Heptagon()
    deltas = [
        {'risk_error': 0.1, 'reward_error': -0.05, 'sentiment_accuracy': 0.8},
        {'risk_error': 0.15, 'reward_error': 0.02, 'sentiment_accuracy': 0.75},
    ]
    h.calibrate(deltas)
    # Just verify no error
    assert len(h._calibration_history) == 1
