"""API REST de scoring (FastAPI) con versionado y health check."""

from fastapi import APIRouter


class ScoreService:
    """Lógica de scoring reutilizada por los endpoints de la API."""

    def __init__(self, registry, feature_store):
        self.registry = registry
        self.feature_store = feature_store

    def score_risk(self, cliente_id: str) -> dict:
        """Score on-demand de riesgo con explicación."""
        raise NotImplementedError

    def score_fraud(self, transaccion: dict) -> dict:
        """Score en tiempo real de fraude con decisión y razones."""
        raise NotImplementedError


router = APIRouter()


@router.post("/v1/risk/score")
def risk_score(request: dict):
    """Endpoint versionado de riesgo."""
    raise NotImplementedError


@router.post("/v1/fraud/score")
def fraud_score(request: dict):
    """Endpoint versionado de fraude."""
    raise NotImplementedError


@router.get("/v1/models")
def list_models():
    """Versiones activas y health de modelos."""
    raise NotImplementedError
