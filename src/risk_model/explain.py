"""Explicabilidad del modelo de riesgo (SHAP global y local)."""


class RiskExplainer:
    """Genera explicaciones SHAP globales y por-cliente."""

    def __init__(self, model):
        self.model = model

    def global_importance(self, X) -> list[dict]:
        """Importancia global de features para model card y revisión."""
        raise NotImplementedError

    def local_explanation(self, row) -> dict:
        """Explicación por cliente: top factores con dirección de impacto."""
        raise NotImplementedError
