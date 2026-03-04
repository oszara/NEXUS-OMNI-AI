"""NEXUS Semantic Router — LangChain + Pydantic production-grade version.

Uses LangChain's ChatOllama with format="json" and JsonOutputParser
for reliable structured output. Falls back to lightweight router when
langchain_ollama is not installed.
"""
import json
from utils.logger import get_logger

logger = get_logger("SemanticRouterLC")

# Check if LangChain is available
try:
    from langchain_ollama import ChatOllama
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    from pydantic import BaseModel, Field
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False


if HAS_LANGCHAIN:
    class SkillRoutingDecision(BaseModel):
        """Pydantic schema for LangChain JsonOutputParser."""

        selected_skill: str = Field(
            description="Nombre del skill/agente elegido, o 'default_llm' si ninguno aplica."
        )
        confidence_score: float = Field(
            ge=0.0, le=1.0, description="Nivel de confianza de 0.0 a 1.0"
        )
        reasoning: str = Field(description="Explicacion tecnica de la decision.")
        requires_sandbox: bool = Field(description="True si requiere ejecucion aislada.")


class NexusSemanticRouterLC:
    """Production semantic router using LangChain + Ollama.

    When langchain_ollama is available, uses ChatOllama with format="json"
    and JsonOutputParser for reliable structured output.
    When not available, falls back to the lightweight router.
    """

    CONFIDENCE_THRESHOLD = 0.65

    def __init__(self, model_name: str = "phi3"):
        self.model_name = model_name
        self._chain = None

        if HAS_LANGCHAIN:
            logger.info(f"LangChain router initialized with {model_name}")
            self._init_langchain(model_name)
        else:
            logger.info("langchain_ollama not available — using lightweight router")

    def _init_langchain(self, model_name: str):
        """Initialize the LangChain pipeline."""
        llm = ChatOllama(
            model=model_name,
            temperature=0.1,  # Low temperature for consistent routing decisions
            format="json"     # Forces Ollama to output pure JSON
        )

        parser = JsonOutputParser(pydantic_object=SkillRoutingDecision)

        prompt = PromptTemplate(
            template=(
                "Eres el ENRUTADOR SEMANTICO del ecosistema NEXUS-OMNI-AI.\n"
                "Tu unica funcion es analizar la solicitud y determinar que agente es el adecuado.\n\n"
                "AGENTES DISPONIBLES:\n{skills_metadata_json}\n\n"
                "SOLICITUD DEL USUARIO:\n\"{user_prompt}\"\n\n"
                "REGLAS:\n"
                "1. Asigna un \"confidence_score\" (0.0 a 1.0). Si es menor a 0.65, elige \"default_llm\".\n"
                "2. Evalua si requiere sandbox (codigo de terceros, ejecucion peligrosa).\n"
                "3. Responde UNICAMENTE con JSON valido.\n\n"
                "{format_instructions}"
            ),
            input_variables=["skills_metadata_json", "user_prompt"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        self._chain = prompt | llm | parser

    def route(self, user_prompt: str, available_skills: dict = None) -> dict:
        """Route a user prompt to the best agent.

        Args:
            user_prompt: The user's question or request
            available_skills: Dict of skill names to descriptions (optional)

        Returns:
            Dict with selected_skill, confidence_score, reasoning, requires_sandbox
        """
        if available_skills is None:
            available_skills = {
                "codigo": "Programacion, scripts, debug, APIs",
                "razonamiento": "Logica, matematicas, analisis paso a paso",
                "redaccion": "Textos, resumenes, traduccion, emails",
                "datos": "Estadistica, SQL, graficos, analisis de datos",
                "investigacion": "Busqueda de hechos, verificacion, sintesis",
                "orquestador": "Tareas complejas que necesitan multiples agentes",
            }

        if not HAS_LANGCHAIN or self._chain is None:
            return self._fallback_route(user_prompt)

        try:
            decision = self._chain.invoke({
                "skills_metadata_json": json.dumps(available_skills, indent=2, ensure_ascii=False),
                "user_prompt": user_prompt
            })

            logger.info(
                f"Route: {decision.get('selected_skill', '?')} "
                f"(confidence: {decision.get('confidence_score', 0):.2f})"
            )

            # Apply confidence threshold
            if decision.get("confidence_score", 0) < self.CONFIDENCE_THRESHOLD:
                decision["selected_skill"] = "default_llm"
                decision["reasoning"] = (
                    f"Low confidence ({decision.get('confidence_score', 0):.2f}): "
                    f"{decision.get('reasoning', '')}"
                )

            return decision

        except Exception as e:
            logger.error(f"LangChain router error: {e}")
            return self._fallback_route(user_prompt)

    def _fallback_route(self, user_prompt: str) -> dict:
        """Fallback when LangChain is not available or fails."""
        logger.info("Using fallback routing (default_llm)")
        return {
            "selected_skill": "default_llm",
            "confidence_score": 0.0,
            "reasoning": "Fallback: LangChain not available or parse error.",
            "requires_sandbox": False
        }


def create_router(model_name: str = "phi3"):
    """Factory function — returns the best available router.

    Returns NexusSemanticRouterLC (which uses LangChain if available,
    or falls back to lightweight routing internally).
    """
    return NexusSemanticRouterLC(model_name=model_name)
