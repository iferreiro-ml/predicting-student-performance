"""
This is a boilerplate pipeline 'modelling'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import upsample_minority_class

def create_upsampling_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=upsample_minority_class,
                inputs=["features_q_train", "labels_q_train"],
                outputs=["upsampled_features_q_train", "upsampled_labels_q_train"],
                name="upsampling_pipeline",
            ),
        ]
    )
