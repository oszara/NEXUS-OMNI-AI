"""Tests for HeuristicEngine."""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.heuristic_engine import HeuristicEngine


@pytest.fixture
def engine():
    return HeuristicEngine()


def test_python_code_routes_to_codigo(engine):
    prompt = "Escribe un script en python con debug api que corrija el código"
    result = engine.route(prompt)
    assert result is not None
    assert result.agent == "codigo"
    assert result.confidence >= 0.75
    assert result.source == "heuristic"


def test_math_logic_routes_to_razonamiento(engine):
    prompt = "Demuestra el teorema de Pitágoras paso a paso con lógica matemática"
    result = engine.route(prompt)
    assert result is not None
    assert result.agent == "razonamiento"
    assert result.confidence >= 0.75


def test_email_writing_routes_to_redaccion(engine):
    prompt = "Redacta un email profesional para solicitar una reunión de trabajo"
    result = engine.route(prompt)
    assert result is not None
    assert result.agent == "redaccion"
    assert result.confidence >= 0.75


def test_sql_data_routes_to_datos(engine):
    prompt = "Analiza datos con pandas y numpy, crea un gráfico con estadísticas"
    result = engine.route(prompt)
    assert result is not None
    assert result.agent == "datos"
    assert result.confidence >= 0.75


def test_research_routes_to_investigacion(engine):
    prompt = "Investiga cuál es la diferencia entre machine learning e inteligencia artificial"
    result = engine.route(prompt)
    assert result is not None
    assert result.agent == "investigacion"
    assert result.confidence >= 0.75


def test_ambiguous_prompt_returns_none(engine):
    # This prompt matches both codigo and investigacion with similar counts
    result = engine.route("hola")
    assert result is None


def test_short_generic_prompt_returns_none(engine):
    result = engine.route("ayuda")
    assert result is None


def test_multiple_patterns_increases_confidence(engine):
    # Many codigo patterns
    prompt = "def fibonacci(): import python class script api debug git"
    result = engine.route(prompt)
    assert result is not None
    assert result.agent == "codigo"
    assert result.confidence == 0.90  # high confidence from many matches


def test_spanish_function_prompt_routes_to_codigo(engine):
    prompt = "escribe una función que calcule fibonacci en python con script"
    result = engine.route(prompt)
    assert result is not None
    assert result.agent == "codigo"


def test_no_match_returns_none(engine):
    result = engine.route("¿Qué tal estás hoy?")
    assert result is None
