"""Hybrid router: heuristic → embedding → LLM fallback cascade."""
import json

try:
    import ollama as ollama_client
except ImportError:
    ollama_client = None

from schemas.routing_schema import RoutingDecision
from core.heuristic_engine import HeuristicEngine
from core.embedding_engine import EmbeddingEngine


class HybridRouter:
    """Three-tier cascading router with increasing latency/accuracy."""

    LLM_SYSTEM_PROMPT = (
        "Eres el NEXUS Semantic Router. "
        "Analiza el prompt del usuario y responde SOLO con JSON válido:\n\n"
        '{"agent": "...", "confidence": 0.0-1.0, '
        '"requires_sandbox": true/false, '
        '"reasoning": "breve explicación"}\n\n'
        "Agentes disponibles:\n"
        "- codigo: programación, scripts, debug, APIs\n"
        "- razonamiento: lógica, matemáticas, análisis paso a paso\n"
        "- redaccion: textos, resúmenes, traducción, emails\n"
        "- datos: estadística, SQL, gráficos, análisis de datos\n"
        "- investigacion: búsqueda de hechos, verificación, síntesis\n"
        "- fallback: cuando ningún agente especializado aplica\n\n"
        "Responde ÚNICAMENTE con el JSON. Sin markdown, sin explicaciones."
    )

    VALID_AGENTS = {"codigo", "razonamiento", "redaccion", "datos", "investigacion", "orquestador", "fallback"}
    MIN_LLM_CONFIDENCE_THRESHOLD = 0.65  # Below this, downgrade to fallback agent

    def __init__(self, llm_model: str = "phi3"):
        self.heuristic = HeuristicEngine()
        self.embedding = EmbeddingEngine()
        self.llm_model = llm_model

    def route(self, prompt: str) -> RoutingDecision:
        """Route through cascading tiers: heuristic → embedding → LLM → fallback."""

        # Tier 1: Heuristic (~0ms)
        decision = self.heuristic.route(prompt)
        if decision is not None:
            return decision

        # Tier 2: Embedding (~5ms)
        decision = self.embedding.route(prompt)
        if decision is not None:
            return decision

        # Tier 3: LLM classification (~500ms-2s)
        decision = self._llm_classify(prompt)
        if decision is not None:
            return decision

        # Tier 4: Fallback
        return RoutingDecision(
            agent="fallback",
            confidence=0.0,
            requires_sandbox=False,
            reasoning="All routing tiers failed — using fallback",
            source="fallback",
        )

    def _llm_classify(self, prompt: str) -> RoutingDecision | None:
        """Use Ollama LLM for classification. Returns None on failure."""
        if ollama_client is None:
            return None

        try:
            response = ollama_client.chat(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": self.LLM_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                options={"num_predict": 256},
            )
            raw = response["message"]["content"].strip()

            # Strip markdown fences
            if raw.startswith("```"):
                lines = raw.split("\n")
                raw = "\n".join(
                    lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
                )

            # Extract JSON
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start >= 0 and end > start:
                parsed = json.loads(raw[start:end])
                # Validate agent name
                agent = parsed.get("agent", "fallback")
                if agent not in self.VALID_AGENTS:
                    agent = "fallback"
                confidence = float(parsed.get("confidence", 0.5))
                confidence = max(0.0, min(1.0, confidence))

                # Downgrade low confidence to fallback
                if confidence < self.MIN_LLM_CONFIDENCE_THRESHOLD:
                    agent = "fallback"

                return RoutingDecision(
                    agent=agent,
                    confidence=confidence,
                    requires_sandbox=bool(parsed.get("requires_sandbox", False)),
                    reasoning=parsed.get("reasoning", "LLM classification"),
                    source="llm",
                )
        except Exception:
            pass

        return None
