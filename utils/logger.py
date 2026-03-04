"""Structured logging for NEXUS-OMNI-AI."""
import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Create a namespaced logger for NEXUS modules.

    Args:
        name: Module name (e.g., "NexusSandbox", "SemanticRouter")
        level: Logging level (default: INFO)

    Returns:
        Configured logger with console handler and structured format.
    """
    logger = logging.getLogger(f"NEXUS.{name}")

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(name)s | %(levelname)s | %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger
