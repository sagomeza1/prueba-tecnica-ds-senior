"""Cliente de métricas (Prometheus) para exponer latencia, throughput y errores."""
from dataclasses import dataclass


@dataclass
class ScoreMetric:
    """Una métrica observada durante el scoring."""
    name: str
    value: float
    labels: dict


class MetricsClient:
    """Encola y envía métricas al pushgateway / endpoint de Prometheus."""

    def record_latency(self, model: str, ms: float) -> None:
        raise NotImplementedError

    def record_score(self, model: str, score: float) -> None:
        raise NotImplementedError

    def record_error(self, model: str, error_type: str) -> None:
        raise NotImplementedError
