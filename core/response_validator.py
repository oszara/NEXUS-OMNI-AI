"""Deterministic response validator — no LLM calls."""
import re


class ResponseValidator:
    """Validates agent responses without calling any LLM.

    Returns (is_valid, reason) tuple.
    """

    MIN_LENGTH = 30
    MAX_ECHO_SIMILARITY = 0.85
    MIN_SENTENCE_LENGTH = 10  # Minimum chars to consider a sentence fragment
    MIN_EXTRA_CONTENT_LENGTH = 20  # Minimum extra chars after prompt to not be an echo

    # Multi-language refusal patterns
    REFUSAL_PATTERNS = [
        r"\bno puedo\b",
        r"\bno tengo capacidad\b",
        r"\bi cannot\b",
        r"\bi can'?t\b",
        r"\bno es posible\b",
        r"\bfuera de mi\b.*\bcapacidad\b",
        r"\bno estoy capacitado\b",
        r"\bsorry\b.*\bcan'?t\b",
    ]

    # Error patterns that should not be shown to users
    ERROR_PATTERNS = [
        r"\[Error",
        r"connection refused",
        r"ConnectionError",
        r"Traceback \(most recent",
        r"HTTPError",
        r"timeout",
        r"ECONNREFUSED",
        r"model.*not found",
    ]

    def validate(self, prompt: str, response: str) -> tuple[bool, str]:
        """Validate a response. Returns (is_valid, reason)."""

        # 1. Empty or too short
        if not response or len(response.strip()) < self.MIN_LENGTH:
            return False, "too_short"

        response_stripped = response.strip()

        # 2. Response is just an echo of the prompt
        if self._is_echo(prompt, response_stripped):
            return False, "echo"

        # 3. Refusal patterns
        response_lower = response_stripped.lower()
        for pattern in self.REFUSAL_PATTERNS:
            if re.search(pattern, response_lower):
                return False, "refusal"

        # 4. Exposed errors
        for pattern in self.ERROR_PATTERNS:
            if re.search(pattern, response_stripped, re.IGNORECASE):
                return False, "error_exposed"

        # 5. Repetitive garbage (same sentence repeated 3+ times)
        sentences = [s.strip() for s in re.split(r'[.!?]\s+', response_stripped) if len(s.strip()) > self.MIN_SENTENCE_LENGTH]
        if len(sentences) >= 3:
            from collections import Counter
            counts = Counter(sentences)
            most_common_count = counts.most_common(1)[0][1] if counts else 0
            if most_common_count >= 3:
                return False, "repetitive"

        return True, "ok"

    def _is_echo(self, prompt: str, response: str) -> bool:
        """Check if response is just echoing the prompt."""
        prompt_clean = prompt.strip().lower()
        response_clean = response.strip().lower()

        if prompt_clean == response_clean:
            return True

        # Check if response starts with the exact prompt and adds nothing substantial
        if response_clean.startswith(prompt_clean):
            extra = response_clean[len(prompt_clean):].strip()
            if len(extra) < self.MIN_EXTRA_CONTENT_LENGTH:
                return True

        return False
