"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import feature_engineering_by_question


def create_pipeline(dataset: str = "train", **kwargs) -> Pipeline:

    fe_pipeline =  Pipeline(
        [
            node(
                func=feature_engineering_by_question,
                inputs=["events", "lk_question"],
                outputs="features_q",
            ),
        ]
    )

    return pipeline(
        pipe=fe_pipeline,
        namespace=f"{dataset}_feature_engineering",
        inputs={"events": f"{dataset}.events_data", "lk_question": "lk_question"},
        outputs={"features_q": f"{dataset}.features_q"},
    )
