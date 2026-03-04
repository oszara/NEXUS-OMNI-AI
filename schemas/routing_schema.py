"""Strict schema for routing decisions."""
from pydantic import BaseModel, Field
from typing import Literal


class RoutingDecision(BaseModel):
    """Validated routing decision from the semantic router."""
    agent: Literal[
        "codigo",
        "razonamiento",
        "redaccion",
        "datos",
        "investigacion",
        "orquestador",
        "fallback"
    ]
    confidence: float = Field(ge=0.0, le=1.0)
    requires_sandbox: bool
    reasoning: str
