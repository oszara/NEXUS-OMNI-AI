"""Model escalation — escalate to more capable model when response is invalid."""


class ModelEscalator:
    """Escalates to a more capable model when the current one fails.

    Instead of asking the same model to 'try again' (which rarely works),
    escalate to a fundamentally more capable model.
    """

    # Escalation chains: current_model → next_model
    ESCALATION_CHAINS = {
        "phi3": "mistral",
        "mistral": "deepseek-r1",
        "qwen3": "deepseek-r1",
        "qwen3-coder": "codestral",
        "codestral": "deepseek-r1",
    }

    def __init__(self, available_models_fn=None):
        """
        Args:
            available_models_fn: Callable that returns list of installed model names.
                                 Signature: () -> list[str]
        """
        self._available_fn = available_models_fn

    def get_escalation(self, current_model: str) -> str | None:
        """Get the next model to try. Returns None if no escalation available."""
        next_model = self.ESCALATION_CHAINS.get(current_model)
        if next_model is None:
            return None

        # Check if the escalation target is actually installed
        if self._available_fn is not None:
            available = self._available_fn()
            # Match by prefix (e.g., "deepseek-r1" matches "deepseek-r1:latest")
            if not any(m.startswith(next_model) for m in available):
                return None

        return next_model

    def escalate(self, agent_key: str, current_model: str, prompt: str,
                 system: str, ollama_fn=None) -> str | None:
        """Try to get a response from the escalation model.

        Args:
            agent_key: Agent identifier (e.g., "codigo")
            current_model: Model that produced the bad response
            prompt: User's original prompt
            system: System prompt for the agent
            ollama_fn: Callable with signature (model, system, prompt) -> str

        Returns:
            New response string, or None if escalation not possible.
        """
        next_model = self.get_escalation(current_model)
        if next_model is None:
            return None

        if ollama_fn is None:
            return None

        try:
            return ollama_fn(next_model, system, prompt)
        except Exception:
            return None
