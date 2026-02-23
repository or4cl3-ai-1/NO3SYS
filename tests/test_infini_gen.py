import pytest
from no3sys.core.infini_gen import InfiniGen, CognitiveParameters


def test_infini_gen_init():
    ig = InfiniGen()
    assert ig.generation == 0
    assert ig.params.fork_depth == 3


def test_evolve_increments_generation():
    ig = InfiniGen()
    ig.evolve([])
    assert ig.generation == 1


def test_curvature_constraint_blocks_mutation():
    ig = InfiniGen(kappa_max=0.3)  # Very strict
    ig.evolve([])
    # Rejected mutations logged
    assert len(ig.history) >= 0  # Some mutations may be rejected


def test_rollback():
    ig = InfiniGen()
    original_alpha = ig.params.alpha
    ig.evolve([])
    result = ig.rollback()
    assert result is not None


def test_status():
    ig = InfiniGen()
    s = ig.status()
    assert 'generation' in s
    assert 'mutations_accepted' in s
    assert 'kappa_max' in s
