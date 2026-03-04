"""Semantic intent classification using Ollama."""
import json
try:
    import ollama
except ImportError:
    ollama = None

from schemas.routing_schema import RoutingDecision


class IntentClassifier:
    """Classifies user intent into the appropriate NEXUS agent."""

    SYSTEM_PROMPT = (
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
        "- orquestador: tareas complejas que necesitan múltiples agentes\n"
        "- fallback: cuando ningún agente especializado aplica\n\n"
        "Responde ÚNICAMENTE con el JSON. Sin markdown, sin explicaciones."
    )

    def __init__(self, model: str = "phi3"):
        self.model = model

    def classify(self, prompt: str) -> RoutingDecision:
        """Classify a user prompt into a routing decision."""
        if ollama is None:
            return RoutingDecision(
                agent="fallback",
                confidence=0.0,
                requires_sandbox=False,
                reasoning="ollama package not available"
            )

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                options={"num_predict": 256}
            )
            raw = response["message"]["content"]
            # Extract JSON from response (handle markdown fences)
            text = raw.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
            # Find JSON object boundaries
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                parsed = json.loads(text[start:end])
                return RoutingDecision(**parsed)
        except Exception:
            pass

        return RoutingDecision(
            agent="fallback",
            confidence=0.0,
            requires_sandbox=False,
            reasoning="Failed to parse classifier response"
        )
