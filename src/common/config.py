"""Carga y valida configuración por entorno (dev/staging/prod).

La configuración vive en configs/<entorno>.yaml y se valida con pydantic
para fallar temprano ante configuraciones inválidas.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    """Configuración de un modelo registrado."""
    name: str
    version: str
    threshold: float


@dataclass(frozen=True)
class ServingConfig:
    """Configuración de serving (host, timeout, replicas)."""
    host: str
    port: int
    timeout_ms: int


class ConfigLoader:
    """Carga configuraciones por entorno y las valida."""

    def __init__(self, env: str, base_path: str):
        self.env = env
        self.base_path = base_path

    def load(self) -> dict:
        """Lee el YAML del entorno y lo valida contra el esquema."""
        raise NotImplementedError

    def get_model(self, name: str) -> ModelConfig:
        """Devuelve la configuración de un modelo específico."""
        raise NotImplementedError
