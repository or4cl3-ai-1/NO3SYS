import pytest
from no3sys.core.fork import Fork, AffectiveState, PredictiveVector
import numpy as np


def test_affective_state_defaults():
    a = AffectiveState()
    assert 0.0 <= a.trust <= 1.0
    assert 0.0 <= a.fear <= 1.0


def test_affective_state_vector():
    a = AffectiveState(trust=0.8, fear=0.1, urgency=0.3, satisfaction=0.7, frustration=0.1)
    v = a.to_vector()
    assert len(v) == 5
    assert v[0] == 0.8


def test_affective_state_roundtrip():
    a = AffectiveState(trust=0.6, fear=0.2, urgency=0.4, satisfaction=0.8, frustration=0.15)
    v = a.to_vector()
    a2 = AffectiveState.from_vector(v)
    assert abs(a2.trust - a.trust) < 1e-6


def test_predictive_vector():
    p = PredictiveVector(risk=0.2, reward=0.8, volatility=0.3, stability=0.7)
    v = p.to_vector()
    assert len(v) == 4
    assert v[1] == 0.8


def test_fork_score():
    f = Fork(
        hypothesis="test",
        confidence=0.8,
        curvature=0.1,
    )
    f.affective_state = AffectiveState(trust=0.8, satisfaction=0.7, fear=0.1, frustration=0.1, urgency=0.3)
    f.predictive_vector = PredictiveVector(reward=0.7, stability=0.8, risk=0.2, volatility=0.2)
    score = f.score()
    assert score > 0.5


def test_fork_to_dict():
    f = Fork(hypothesis="hello")
    d = f.to_dict()
    assert 'fork_id' in d
    assert 'sentiment' in d
    assert 'future' in d
    assert 'confidence' in d
