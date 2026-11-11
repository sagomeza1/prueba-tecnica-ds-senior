"""Pipeline de entrenamiento del modelo de fraude (híbrido)."""


class FraudModelTrainer:
    """Entrena modelos no supervisado (anomalías) y supervisado (fraude)."""

    def __init__(self, mlflow_tracking_uri: str):
        self.mlflow_tracking_uri = mlflow_tracking_uri

    def train_unsupervised(self, X) -> "AnomalyModel":
        """Isolation Forest / autoencoder para anomalías sin etiqueta."""
        raise NotImplementedError

    def train_supervised(self, X, y) -> "FraudModel":
        """GBM sobre fraudes confirmados (con manejo de desbalance)."""
        raise NotImplementedError

    def build_ensemble(self, anomaly, fraud, rules) -> "EnsembleModel":
        """Combina anomalía + fraude + reglas en un score combinado."""
        raise NotImplementedError

    def calibrate_threshold(self, model, X, y, cost_fp: float, cost_fn: float) -> float:
        """Calibra el umbral de alerta contra costo de FP vs FN."""
        raise NotImplementedError
