"""Logging estructurado (JSON) con contexto de run/modelo para trazabilidad."""
import logging


class JsonLogger:
    """Logger JSON con campos de contexto obligatorios (run_id, modelo, entorno)."""

    def __init__(self, context: dict):
        self.context = context

    def info(self, msg: str, **fields) -> None:
        raise NotImplementedError

    def error(self, msg: str, exc: Exception | None = None, **fields) -> None:
        raise NotImplementedError
