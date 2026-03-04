"""Tests for the LangChain semantic router."""
import pytest
from core.semantic_router_langchain import NexusSemanticRouterLC, create_router, HAS_LANGCHAIN


class TestRouterFactory:
    def test_create_router_returns_instance(self):
        router = create_router("phi3")
        assert isinstance(router, NexusSemanticRouterLC)

    def test_fallback_route_returns_default(self):
        router = NexusSemanticRouterLC(model_name="phi3")
        result = router._fallback_route("test prompt")
        assert result["selected_skill"] == "default_llm"
        assert result["confidence_score"] == 0.0
        assert result["requires_sandbox"] is False


class TestRouterDecisions:
    def test_route_returns_dict_keys(self):
        router = create_router("phi3")
        result = router.route("hello world")
        assert "selected_skill" in result
        assert "confidence_score" in result
        assert "reasoning" in result
        assert "requires_sandbox" in result


if HAS_LANGCHAIN:
    from core.semantic_router_langchain import SkillRoutingDecision

    class TestSkillRoutingDecision:
        def test_valid_decision(self):
            d = SkillRoutingDecision(
                selected_skill="codigo",
                confidence_score=0.9,
                reasoning="test",
                requires_sandbox=False
            )
            assert d.selected_skill == "codigo"

        def test_confidence_bounds(self):
            with pytest.raises(Exception):
                SkillRoutingDecision(
                    selected_skill="x",
                    confidence_score=1.5,
                    reasoning="x",
                    requires_sandbox=False
                )
