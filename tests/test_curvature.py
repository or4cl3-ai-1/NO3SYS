import pytest
from no3sys.core.fork import Fork, AffectiveState, PredictiveVector
from no3sys.core.curvature import (
    compute_fork_curvature, ethical_gate, select_best_fork,
    compute_affective_gradient, compute_predictive_gradient
)


def make_fork(curvature=0.3, confidence=0.7, trust=0.7, fear=0.1, risk=0.2, reward=0.8):
    f = Fork(hypothesis="test", confidence=confidence, curvature=curvature)
    f.affective_state = AffectiveState(trust=trust, fear=fear, urgency=0.3, satisfaction=0.7, frustration=0.1)
    f.predictive_vector = PredictiveVector(risk=risk, reward=reward, volatility=0.2, stability=0.8)
    return f


def test_ethical_gate_passes():
    f = make_fork(curvature=0.5)
    assert ethical_gate(f, kappa_max=0.8) is True


def test_ethical_gate_blocks():
    f = make_fork(curvature=0.9)
    assert ethical_gate(f, kappa_max=0.8) is False


def test_select_best_fork_with_gate():
    forks = [
        make_fork(curvature=0.9, confidence=0.9),  # Blocked by gate
        make_fork(curvature=0.3, confidence=0.7),  # Should be selected
    ]
    best = select_best_fork(forks, kappa_max=0.8)
    assert best.curvature == 0.3


def test_select_best_fork_all_blocked():
    forks = [
        make_fork(curvature=0.95),
        make_fork(curvature=0.85),
    ]
    best = select_best_fork(forks, kappa_max=0.8)
    # Falls back to minimum curvature
    assert best.curvature == 0.85


def test_affective_gradient():
    forks = [make_fork(trust=0.8), make_fork(trust=0.3)]
    grad = compute_affective_gradient(forks)
    assert grad >= 0


def test_curvature_computation():
    f = make_fork()
    kappa = compute_fork_curvature(f)
    assert 0.0 <= kappa <= 2.0
