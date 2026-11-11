"""Pipeline de entrenamiento del modelo de riesgo financiero.

Entrena GBM (LightGBM/XGBoost) con baseline de regresión logística,
valida con CV temporal y registra en MLflow.
"""


class RiskModelTrainer:
    """Entrena, evalúa y registra el modelo de riesgo."""

    def __init__(self, mlflow_tracking_uri: str):
        self.mlflow_tracking_uri = mlflow_tracking_uri

    def load_training_data(self, feature_store, start: str, end: str):
        """Carga features offline y target (default a 90+ días)."""
        raise NotImplementedError

    def build_pipeline(self, params: dict):
        """Construye el pipeline de preprocesamiento + modelo."""
        raise NotImplementedError

    def train(self, X, y) -> "Model":
        """Entrena con validación cruzada temporal (walk-forward)."""
        raise NotImplementedError

    def evaluate(self, model, X, y) -> dict:
        """Calcula AUC, KS, Gini, precision@k, calibración y PSI."""
        raise NotImplementedError

    def register(self, model, metrics: dict, params: dict) -> str:
        """Registra modelo + artefactos + métricas en MLflow y devuelve versión."""
        raise NotImplementedError
