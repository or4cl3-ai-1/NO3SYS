import pytest
from no3sys import NO3SYS


@pytest.fixture
def system():
    return NO3SYS(fork_depth=3, kappa_max=0.8, auto_evolve=False)


def test_system_initializes(system):
    assert system.VERSION == "1.0.0"
    assert system.session_id is not None


def test_process_returns_response(system):
    result = system.process("What is geometric cognition?")
    assert "response" in result
    assert len(result["response"]) > 0


def test_process_generates_forks(system):
    result = system.process("Explain fork-based reasoning")
    assert result["fork_count"] == 3


def test_process_has_valid_confidence(system):
    result = system.process("Test query")
    assert 0.0 <= result["ensemble_confidence"] <= 1.0


def test_process_selected_fork_has_curvature(system):
    result = system.process("Ethical AI development")
    assert "curvature" in result["selected_fork"]
    assert 0.0 <= result["selected_fork"]["curvature"] <= 2.0


def test_remember_and_recall(system):
    system.remember("test_key", "test_value", confidence=0.9)
    val = system.square.recall("test_key")
    assert val == "test_value"


def test_validate_outcome(system):
    result = system.process("test query")
    fork_id = result["selected_fork"]["fork_id"]
    validation = system.validate_outcome(fork_id, {
        "risk": 0.3,
        "reward": 0.7,
        "sentiment_quality": 0.8,
        "harm": 0.1
    })
    assert validation.get("validated") is True


def test_status(system):
    system.process("status test")
    status = system.status()
    assert status["cycles_completed"] == 1
    assert status["total_forks"] == 3


def test_auto_evolve_triggers(system):
    system.auto_evolve = True
    for _ in range(5):
        system.process("evolution test query")
    status = system.status()
    assert status["infini_gen"]["generation"] >= 1
