"""Tests for the NEXUS Orchestrator."""
from core.orchestrator import NexusOrchestrator


class TestOrchestratorInit:
    def test_creates_router_and_sandbox(self):
        orch = NexusOrchestrator(model_name="phi3")
        assert orch.router is not None
        assert orch.sandbox is not None

    def test_register_skill(self):
        orch = NexusOrchestrator()
        orch.register_skill("test_skill", "/path/to/script.py", trusted=False)
        assert "test_skill" in orch.skill_registry
        assert orch.skill_registry["test_skill"]["trusted"] is False

    def test_process_with_no_handler_returns_fallback(self):
        orch = NexusOrchestrator()
        result = orch.process_request("hello")
        assert result["agent"] == "default_llm"

    def test_process_with_default_handler(self):
        orch = NexusOrchestrator()
        result = orch.process_request(
            "hello",
            default_handler=lambda p: f"Response to: {p}"
        )
        assert result["status"] == "success"
        assert "Response to: hello" in result["data"]
