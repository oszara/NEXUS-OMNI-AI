"""Tests for the NEXUS Semantic Skill Router."""
import pytest
from schemas.routing_schema import RoutingDecision
from core.risk_analyzer import RiskAnalyzer
from core.semantic_router import SemanticRouter


class TestRoutingDecision:
    def test_valid_decision(self):
        d = RoutingDecision(agent="codigo", confidence=0.9, requires_sandbox=False, reasoning="test")
        assert d.agent == "codigo"
        assert d.confidence == 0.9

    def test_invalid_agent_rejected(self):
        with pytest.raises(Exception):
            RoutingDecision(agent="invalid_agent", confidence=0.5, requires_sandbox=False, reasoning="x")

    def test_confidence_bounds(self):
        with pytest.raises(Exception):
            RoutingDecision(agent="codigo", confidence=1.5, requires_sandbox=False, reasoning="x")
        with pytest.raises(Exception):
            RoutingDecision(agent="codigo", confidence=-0.1, requires_sandbox=False, reasoning="x")


class TestRiskAnalyzer:
    def setup_method(self):
        self.analyzer = RiskAnalyzer()

    def test_safe_prompt(self):
        assert not self.analyzer.requires_sandbox("Write a Python hello world")

    def test_os_system(self):
        assert self.analyzer.requires_sandbox("use os.system to delete files")

    def test_subprocess(self):
        assert self.analyzer.requires_sandbox("run subprocess.call(['rm', '-rf'])")

    def test_eval(self):
        assert self.analyzer.requires_sandbox("eval(user_input)")

    def test_exec(self):
        assert self.analyzer.requires_sandbox("exec(code)")

    def test_rm_rf(self):
        assert self.analyzer.requires_sandbox("rm -rf /")

    def test_sql_injection(self):
        assert self.analyzer.requires_sandbox("DROP TABLE users")

    def test_sudo(self):
        assert self.analyzer.requires_sandbox("sudo rm -rf /")


class TestSemanticRouter:
    def test_low_confidence_fallback(self):
        """Router should return fallback when confidence is below threshold."""
        router = SemanticRouter()
        # Monkey-patch classifier to return low confidence
        original = router.classifier.classify
        router.classifier.classify = lambda p: RoutingDecision(
            agent="codigo", confidence=0.3, requires_sandbox=False, reasoning="test"
        )
        result = router.route("test prompt")
        assert result.agent == "fallback"
        router.classifier.classify = original

    def test_sandbox_override(self):
        """Risk analyzer should override requires_sandbox even if classifier says False."""
        router = SemanticRouter()
        router.classifier.classify = lambda p: RoutingDecision(
            agent="codigo", confidence=0.9, requires_sandbox=False, reasoning="test"
        )
        result = router.route("use eval(input()) to process data")
        assert result.requires_sandbox is True
