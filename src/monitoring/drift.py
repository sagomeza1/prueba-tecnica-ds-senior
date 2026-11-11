"""Detección de data drift (PSI/KS) y concept drift (degradación)."""


class DriftMonitor:
    """Calcula PSI/KS de features y detecta degradación de performance."""

    def __init__(self, reference: dict, current: dict):
        self.reference = reference
        self.current = current

    def psi(self, feature: str) -> float:
        """Population Stability Index de una feature."""
        raise NotImplementedError

    def ks_drift(self, feature: str) -> float:
        """KS entre distribución actual y de referencia."""
        raise NotImplementedError

    def performance_delta(self, metric: str) -> float:
        """Variación de métrica (AUC/precision) vs. referencia."""
        raise NotImplementedError

    def should_alert(self, feature: str, threshold: float = 0.2) -> bool:
        """Decide si el drift supera el umbral de alerta."""
        raise NotImplementedError
