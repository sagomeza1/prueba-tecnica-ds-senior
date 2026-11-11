"""Cliente del Feature Store (Feast) para consistencia online/offline.

Garantiza que las features usadas en entrenamiento sean las mismas que en
serving, evitando train/serve skew.
"""


class FeatureStoreClient:
    """Lee features online (Redis) y materializa features offline (parquet)."""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def get_online_features(self, entity_rows: list[dict]) -> dict:
        """Devuelve features en tiempo real para scoring online."""
        raise NotImplementedError

    def materialize(self, start: str, end: str) -> None:
        """Materializa features offline para entrenamiento batch."""
        raise NotImplementedError

    def apply_definitions(self) -> None:
        """Aplica definiciones de features versionadas al store."""
        raise NotImplementedError
