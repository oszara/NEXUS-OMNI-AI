"""Deterministic heuristic-based routing — zero latency."""
import re
from schemas.routing_schema import RoutingDecision


class HeuristicEngine:
    """Fast pattern-matching router. Returns None if no pattern matches with high confidence."""

    PATTERNS = {
        "codigo": [
            r"\bdef\b", r"\bclass\b", r"\bimport\b", r"\bfunction\b",
            r"```", r"\bpython\b", r"\bjavascript\b", r"\bjava\b", r"\bsql\b",
            r"\bapi\b", r"\bdebug\b", r"\berror\b.*código", r"\bscript\b",
            r"\bprograma\b.*que", r"\bcódigo\b", r"\bfunción\b.*que",
            r"\bcorrige\b.*código", r"\brefactori", r"\bgit\b",
        ],
        "razonamiento": [
            r"\bexplica\b.*paso", r"\bpor\s+qué\b", r"\bdemuestra\b",
            r"\blógica\b", r"\bmatemátic", r"\bcalcula\b", r"\banaliza\b.*lógic",
            r"\bpaso\s+a\s+paso\b", r"\bradical\b", r"\bderivada\b",
            r"\bintegral\b", r"\becuación\b", r"\bteorema\b",
        ],
        "redaccion": [
            r"\bescribe\b.*email", r"\bredacta\b", r"\btraduce\b",
            r"\bresume\b", r"\bresumen\b", r"\bcarta\b", r"\bensayo\b",
            r"\btexto\b.*profesional", r"\bcorrige\b.*texto",
            r"\bmejora\b.*redacción", r"\bemail\b", r"\binforme\b",
        ],
        "datos": [
            r"\bSELECT\b", r"\bGROUP\s+BY\b", r"\bJOIN\b",
            r"\bdataframe\b", r"\bestadístic", r"\bgráfico\b",
            r"\bcsv\b", r"\bexcel\b", r"\bpandas\b", r"\bnumpy\b",
            r"\banálisis\b.*datos", r"\bregresión\b", r"\bcorrelación\b",
        ],
        "investigacion": [
            r"\binvestiga\b", r"\bbusca\b.*información",
            r"\bverifica\b", r"\bcompara\b.*entre",
            r"\bqué\s+es\b", r"\bcuál\s+es\b", r"\bhistoria\b.*de\b",
            r"\bdefinición\b", r"\bdiferencia\b.*entre",
        ],
    }

    # Minimum number of pattern matches to be confident
    MIN_MATCHES_HIGH = 3   # confidence 0.90
    MIN_MATCHES_MED = 2    # confidence 0.75
    MIN_MATCHES_LOW = 1    # confidence 0.60 — not enough, return None

    def route(self, prompt: str) -> RoutingDecision | None:
        """Try to route using heuristics. Returns None if not confident enough."""
        scores = {}
        prompt_lower = prompt.lower()

        for agent, patterns in self.PATTERNS.items():
            count = sum(1 for p in patterns if re.search(p, prompt_lower))
            if count > 0:
                scores[agent] = count

        if not scores:
            return None

        best_agent = max(scores, key=scores.get)
        best_count = scores[best_agent]

        if best_count >= self.MIN_MATCHES_HIGH:
            confidence = 0.90
        elif best_count >= self.MIN_MATCHES_MED:
            confidence = 0.75
        else:
            # Only 1 match — not confident enough for heuristic
            return None

        # Check for ambiguity: if second-best is close, don't decide
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) >= 2 and sorted_scores[0] - sorted_scores[1] <= 1:
            return None  # Ambiguous — let embedding/LLM decide

        return RoutingDecision(
            agent=best_agent,
            confidence=confidence,
            requires_sandbox=False,
            reasoning=f"Heuristic: {best_count} pattern matches for '{best_agent}'",
            source="heuristic",
        )
