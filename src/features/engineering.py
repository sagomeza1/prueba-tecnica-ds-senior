"""Feature engineering: agregaciones temporales, ratios y encodings.

Cada transformación es una función pura (dataframe -> dataframe) para
reproducibilidad y testabilidad. El target encoding se hace out-of-fold
para evitar leakage.
"""


class FeatureEngineer:
    """Aplica transformaciones de features sobre datos batch/offline."""

    def add_rolling_aggregates(self, df, windows: list[int]) -> "DataFrame":
        """Agrega sumas/medias/medians en ventanas (3/6/12 meses)."""
        raise NotImplementedError

    def add_ratios(self, df, num: str, den: str, name: str):
        """Crea ratios (p. ej. utilización/cupo)."""
        raise NotImplementedError

    def target_encode_oof(self, df, col: str, target: str, folds: int):
        """Target encoding out-of-fold para categóricas de alta cardinalidad."""
        raise NotImplementedError
