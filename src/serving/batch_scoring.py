"""Scoring batch de la cartera de riesgo (Spark)."""


class RiskBatchScorer:
    """Re-scoreo mensual/semanal de toda la cartera en Spark."""

    def __init__(self, spark, registry, feature_store):
        self.spark = spark
        self.registry = registry
        self.feature_store = feature_store

    def score_portfolio(self, start: str, end: str) -> "DataFrame":
        """Aplica el modelo vigente a la cartera y escribe resultados."""
        raise NotImplementedError
