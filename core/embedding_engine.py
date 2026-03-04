"""Embedding-based semantic routing using sentence-transformers."""
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from schemas.routing_schema import RoutingDecision


class EmbeddingEngine:
    """Routes prompts using cosine similarity against agent descriptions."""

    # Bilingual descriptions (Spanish + English keywords) for better matching
    AGENT_DESCRIPTIONS = {
        "codigo": (
            "programación python javascript java sql código depuración software "
            "programming code debug script function class API desarrollo developer "
            "error fix bug compilar ejecutar terminal"
        ),
        "razonamiento": (
            "lógica matemáticas análisis paso a paso razonamiento deducción "
            "logic math reasoning step by step calculate proof theorem "
            "ecuación problema resolver demostrar"
        ),
        "redaccion": (
            "texto redacción escritura resumen traducción email carta ensayo "
            "writing summary translation professional document informe "
            "corregir gramática estilo mejora"
        ),
        "datos": (
            "datos estadística SQL gráfico análisis dataframe pandas numpy "
            "data statistics chart plot csv excel regression correlation "
            "base de datos tabla consulta"
        ),
        "investigacion": (
            "investigación búsqueda hechos verificación síntesis información "
            "research search facts verification synthesis compare "
            "definición historia contexto"
        ),
    }

    CONFIDENCE_THRESHOLD = 0.35  # Below this, return None
    MIN_EMBEDDING_CONFIDENCE = 0.55  # Lower bound for normalized confidence
    MAX_EMBEDDING_CONFIDENCE = 0.85  # Upper bound for normalized confidence

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self._model = None
        self._model_name = model_name
        self._agent_embeddings = {}

    def _ensure_loaded(self) -> bool:
        """Lazy-load model on first use."""
        if self._model is not None:
            return True
        if SentenceTransformer is None:
            return False
        try:
            self._model = SentenceTransformer(self._model_name)
            # Pre-compute agent embeddings
            for agent, desc in self.AGENT_DESCRIPTIONS.items():
                self._agent_embeddings[agent] = self._model.encode(desc, normalize_embeddings=True)
            return True
        except Exception:
            return False

    def route(self, prompt: str) -> RoutingDecision | None:
        """Route using embedding similarity. Returns None if not confident."""
        if not self._ensure_loaded():
            return None

        prompt_embedding = self._model.encode(prompt, normalize_embeddings=True)

        scores = {}
        for agent, agent_emb in self._agent_embeddings.items():
            similarity = float(np.dot(prompt_embedding, agent_emb))
            scores[agent] = similarity

        if not scores:
            return None

        best_agent = max(scores, key=scores.get)
        best_score = scores[best_agent]

        if best_score < self.CONFIDENCE_THRESHOLD:
            return None

        # Normalize score to confidence range [MIN_EMBEDDING_CONFIDENCE, MAX_EMBEDDING_CONFIDENCE]
        confidence = min(self.MAX_EMBEDDING_CONFIDENCE, max(self.MIN_EMBEDDING_CONFIDENCE, best_score))

        return RoutingDecision(
            agent=best_agent,
            confidence=confidence,
            requires_sandbox=False,
            reasoning=f"Embedding similarity: {best_score:.3f} for '{best_agent}'",
            source="embedding",
        )
