"""Tests for ResponseValidator."""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.response_validator import ResponseValidator


@pytest.fixture
def validator():
    return ResponseValidator()


def test_valid_response(validator):
    prompt = "¿Cómo funciona Python?"
    response = "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Se caracteriza por su sintaxis clara y legible."
    is_valid, reason = validator.validate(prompt, response)
    assert is_valid is True
    assert reason == "ok"


def test_empty_response(validator):
    is_valid, reason = validator.validate("prompt", "")
    assert is_valid is False
    assert reason == "too_short"


def test_very_short_response(validator):
    is_valid, reason = validator.validate("prompt", "Ok.")
    assert is_valid is False
    assert reason == "too_short"


def test_echo_of_prompt(validator):
    prompt = "¿Cuál es la capital de Francia?"
    response = "¿Cuál es la capital de Francia?"
    is_valid, reason = validator.validate(prompt, response)
    assert is_valid is False
    assert reason == "echo"


def test_refusal_spanish_no_puedo(validator):
    prompt = "Explícame algo"
    response = "Lo siento, no puedo responder a esa pregunta en este momento."
    is_valid, reason = validator.validate(prompt, response)
    assert is_valid is False
    assert reason == "refusal"


def test_refusal_english_i_cannot(validator):
    prompt = "Tell me something"
    response = "I cannot provide information about that topic as it falls outside my capabilities."
    is_valid, reason = validator.validate(prompt, response)
    assert is_valid is False
    assert reason == "refusal"


def test_error_exposed_traceback(validator):
    prompt = "Ejecuta el código"
    response = "Traceback (most recent call last):\n  File 'script.py', line 5\nNameError: name 'x' is not defined"
    is_valid, reason = validator.validate(prompt, response)
    assert is_valid is False
    assert reason == "error_exposed"


def test_connection_error_exposed(validator):
    prompt = "Consulta la API"
    response = "Error al conectar: connection refused — no se pudo establecer conexión"
    is_valid, reason = validator.validate(prompt, response)
    assert is_valid is False
    assert reason == "error_exposed"


def test_repetitive_garbage(validator):
    prompt = "Explica algo"
    sentence = "Esta es una respuesta repetida sin sentido"
    response = f"{sentence}. {sentence}. {sentence}. {sentence}."
    is_valid, reason = validator.validate(prompt, response)
    assert is_valid is False
    assert reason == "repetitive"


def test_normal_long_response(validator):
    prompt = "¿Qué es la inteligencia artificial?"
    response = (
        "La inteligencia artificial (IA) es un campo de la informática que busca crear sistemas "
        "capaces de realizar tareas que normalmente requieren inteligencia humana. "
        "Esto incluye el aprendizaje automático, el procesamiento del lenguaje natural, "
        "la visión por computadora y la robótica. La IA tiene aplicaciones en medicina, "
        "finanzas, educación y muchas otras áreas."
    )
    is_valid, reason = validator.validate(prompt, response)
    assert is_valid is True
    assert reason == "ok"
