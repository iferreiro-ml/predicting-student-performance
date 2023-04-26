"""
This is a boilerplate pipeline 'reporting'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import overall_performance


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=overall_performance,
                inputs=["y_test", "y_pred"],
                outputs=["overall_metrics", "op_table"],
                name="overall_performance_reporting",
            )
        ]
    )
