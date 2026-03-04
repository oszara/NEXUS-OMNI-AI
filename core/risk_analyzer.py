"""Deterministic risk analysis for sandbox detection."""
import re


class RiskAnalyzer:
    """Detects potentially dangerous patterns in user prompts."""

    CODE_PATTERNS = [
        r"os\.system",
        r"subprocess",
        r"eval\s*\(",
        r"exec\s*\(",
        r"rm\s+-rf",
        r"__import__",
        r"shutil\.rmtree",
        r"open\s*\(.+['\"]w['\"]",
        r"DROP\s+TABLE",
        r"DELETE\s+FROM",
        r"; *rm ",
        r"\bsudo\b",
    ]

    def __init__(self):
        self._compiled = [re.compile(p, re.IGNORECASE) for p in self.CODE_PATTERNS]

    def requires_sandbox(self, prompt: str) -> bool:
        """Return True if the prompt contains potentially dangerous patterns."""
        for pattern in self._compiled:
            if pattern.search(prompt):
                return True
        return False
