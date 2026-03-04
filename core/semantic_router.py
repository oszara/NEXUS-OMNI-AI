"""NEXUS Semantic Skill Router — routes prompts to the best agent."""
from core.intent_classifier import IntentClassifier
from core.risk_analyzer import RiskAnalyzer
from schemas.routing_schema import RoutingDecision


class SemanticRouter:
    """Routes user prompts to the optimal NEXUS agent.

    Uses LLM-based intent classification combined with deterministic
    risk analysis to produce a validated routing decision.
    """

    CONFIDENCE_THRESHOLD = 0.65

    def __init__(self, model: str = "phi3"):
        self.classifier = IntentClassifier(model=model)
        self.risk_analyzer = RiskAnalyzer()

    def route(self, prompt: str) -> RoutingDecision:
        """Analyze a prompt and return a routing decision."""
        decision = self.classifier.classify(prompt)

        # Deterministic sandbox override
        if self.risk_analyzer.requires_sandbox(prompt):
            decision.requires_sandbox = True

        # Low confidence → fallback
        if decision.confidence < self.CONFIDENCE_THRESHOLD:
            decision = RoutingDecision(
                agent="fallback",
                confidence=decision.confidence,
                requires_sandbox=decision.requires_sandbox,
                reasoning=f"Low confidence ({decision.confidence:.2f}): {decision.reasoning}"
            )

        return decision
