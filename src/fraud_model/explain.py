"""Explicabilidad del modelo de fraude: razones legibles para el analista."""


class FraudExplainer:
    """Traduce el score a razones accionables (ej. 'monto 8x mediana')."""

    def __init__(self, model):
        self.model = model

    def reasons(self, transaction_features: dict) -> list[str]:
        """Devuelve razones humanas del porqué se marcó la transacción."""
        raise NotImplementedError
