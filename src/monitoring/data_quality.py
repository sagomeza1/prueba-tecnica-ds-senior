"""Validación de calidad de datos de entrada (Great Expectations)."""


class DataQualityValidator:
    """Valida esquema, nulos, rangos y cardinalidad de features de entrada."""

    def __init__(self, expectations_suite: str):
        self.expectations_suite = expectations_suite

    def validate(self, df) -> dict:
        """Ejecuta la suite de expectativas y devuelve el resultado."""
        raise NotImplementedError

    def critical_failures(self, result: dict) -> list[str]:
        """Lista violaciones críticas que bloquean el scoring."""
        raise NotImplementedError
