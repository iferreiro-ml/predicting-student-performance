"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import feature_engineering_by_question


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([node(
                func=feature_engineering_by_question,
                inputs=["events_train", "labels_q", "lk_question"],
                outputs="primary_q",
            ),])
