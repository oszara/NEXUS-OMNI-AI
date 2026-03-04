"""NEXUS Orchestrator — Unified pipeline: Route -> Sandbox/Direct -> Fallback.

This module provides the top-level request processing logic that:
1. Uses the semantic router to determine the best agent
2. Checks if sandbox execution is required
3. Falls back to multi-agent CrewAI orchestration for complex tasks
"""
from utils.logger import get_logger
from core.sandbox import SandboxManager
from core.semantic_router_langchain import create_router

logger = get_logger("Orchestrator")


class NexusOrchestrator:
    """Central orchestrator that routes, sandboxes, and executes.

    Attributes:
        router: Semantic router (LangChain or lightweight)
        sandbox: SandboxManager for isolated execution
    """

    def __init__(self, model_name: str = "phi3", sandbox_timeout: int = 30):
        self.router = create_router(model_name=model_name)
        self.sandbox = SandboxManager(timeout_seconds=sandbox_timeout)
        self.skill_registry = {}  # Maps skill names to script paths
        logger.info("NexusOrchestrator initialized")

    def register_skill(self, name: str, script_path: str, trusted: bool = True):
        """Register a skill with its execution path.

        Args:
            name: Skill identifier (must match router agent names)
            script_path: Path to the Python script
            trusted: If False, will always use sandbox execution
        """
        self.skill_registry[name] = {
            "path": script_path,
            "trusted": trusted
        }
        logger.info(f"Registered skill: {name} (trusted={trusted})")

    def process_request(self, prompt: str, default_handler=None) -> dict:
        """Process a user request through the full pipeline.

        Args:
            prompt: User's question or command
            default_handler: Callable(prompt) -> str for default LLM fallback

        Returns:
            Dict with 'status', 'agent', 'data' or 'message'
        """
        # 1. Route
        decision = self.router.route(prompt)
        selected = decision.get("selected_skill", "default_llm")
        confidence = decision.get("confidence_score", 0.0)
        needs_sandbox = decision.get("requires_sandbox", False)

        logger.info(f"Routing decision: {selected} (confidence={confidence:.2f}, sandbox={needs_sandbox})")

        # 2. Low confidence or default_llm -> use default handler
        if selected == "default_llm" or confidence < 0.65:
            if default_handler:
                try:
                    result = default_handler(prompt)
                    return {"status": "success", "agent": "default_llm", "data": result}
                except Exception as e:
                    return {"status": "error", "agent": "default_llm", "message": str(e)}
            return {"status": "fallback", "agent": "default_llm", "message": "No default handler configured"}

        # 3. Check if skill is registered
        if selected not in self.skill_registry:
            logger.warning(f"Skill '{selected}' not in registry — falling back")
            if default_handler:
                return {"status": "success", "agent": "default_llm", "data": default_handler(prompt)}
            return {"status": "error", "agent": selected, "message": f"Skill '{selected}' not registered"}

        skill_info = self.skill_registry[selected]

        # 4. Sandbox or direct execution
        if needs_sandbox or not skill_info["trusted"]:
            logger.info(f"Sandbox execution for: {selected}")
            result = self.sandbox.execute_safely(
                skill_info["path"],
                {"prompt": prompt}
            )
            result["agent"] = selected
            return result
        else:
            # Direct execution (trusted internal skills)
            logger.info(f"Direct execution for: {selected}")
            try:
                result = self.sandbox.execute_safely(
                    skill_info["path"],
                    {"prompt": prompt}
                )
                result["agent"] = selected
                return result
            except Exception as e:
                return {"status": "error", "agent": selected, "message": str(e)}
