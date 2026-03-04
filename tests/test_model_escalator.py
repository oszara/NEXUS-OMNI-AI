"""Tests for ModelEscalator."""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.model_escalator import ModelEscalator


@pytest.fixture
def escalator_no_check():
    """Escalator without availability check."""
    return ModelEscalator(available_models_fn=None)


def test_phi3_escalates_to_mistral(escalator_no_check):
    result = escalator_no_check.get_escalation("phi3")
    assert result == "mistral"


def test_mistral_escalates_to_deepseek_r1(escalator_no_check):
    result = escalator_no_check.get_escalation("mistral")
    assert result == "deepseek-r1"


def test_qwen3_coder_escalates_to_codestral(escalator_no_check):
    result = escalator_no_check.get_escalation("qwen3-coder")
    assert result == "codestral"


def test_deepseek_r1_no_escalation(escalator_no_check):
    result = escalator_no_check.get_escalation("deepseek-r1")
    assert result is None


def test_unknown_model_no_escalation(escalator_no_check):
    result = escalator_no_check.get_escalation("unknown-model-xyz")
    assert result is None


def test_escalation_target_not_installed_returns_none():
    # Availability function returns empty list (no models installed)
    escalator = ModelEscalator(available_models_fn=lambda: [])
    result = escalator.get_escalation("phi3")
    assert result is None


def test_escalation_target_installed():
    # Availability function returns the escalation target
    escalator = ModelEscalator(available_models_fn=lambda: ["mistral:latest", "phi3:latest"])
    result = escalator.get_escalation("phi3")
    assert result == "mistral"


def test_escalate_with_mock_ollama_fn(escalator_no_check):
    def mock_ollama(model, system, prompt):
        return f"Response from {model}: {prompt}"

    response = escalator_no_check.escalate(
        agent_key="codigo",
        current_model="phi3",
        prompt="Write a function",
        system="You are a coder",
        ollama_fn=mock_ollama,
    )
    assert response is not None
    assert "mistral" in response


def test_escalate_with_failing_ollama_fn(escalator_no_check):
    def failing_ollama(model, system, prompt):
        raise RuntimeError("Connection failed")

    response = escalator_no_check.escalate(
        agent_key="codigo",
        current_model="phi3",
        prompt="Write a function",
        system="You are a coder",
        ollama_fn=failing_ollama,
    )
    assert response is None


def test_escalate_without_ollama_fn(escalator_no_check):
    response = escalator_no_check.escalate(
        agent_key="codigo",
        current_model="phi3",
        prompt="Write a function",
        system="You are a coder",
        ollama_fn=None,
    )
    assert response is None
