"""
This is a boilerplate pipeline 'ingestion'
generated using Kedro 0.18.6
"""

from .pipeline import new_rmu_pipeline, new_event_features_pipeline, new_qs_pipeline, new_split_pipeline

__all__ = ["new_rmu_pipeline", "new_event_features_pipeline", "new_qs_pipeline", "new_split_pipeline"]

__version__ = "0.1"
