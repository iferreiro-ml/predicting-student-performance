"""
This is a boilerplate pipeline 'ingestion'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from kedro.pipeline.modular_pipeline import pipeline

from ...nodes.time_diff_def import time_diff_def
from ...nodes.reduce_memory_usage import reduce_memory_usage
from ...nodes.question_split import question_split
from .nodes import jo_train_test_split

def new_rmu_pipeline(namespace: str = "train") -> Pipeline:
    """rmu stands for "reduce memory usage"
    This pipeline creates a modular instance that can be applied to
    any event_data DataFrame to type it, thus reducing its memory usage.
    The name of the event_data DataFrame has to be input in the namespace argument 
    """

    rmu_pipeline = pipeline(
        [
            node(
                func=reduce_memory_usage,
                inputs="event_data",
                outputs="light_event_data",
                name="rmu_node",
            ),
        ]
    )

    return pipeline(
        pipe=rmu_pipeline,
        namespace=f"{namespace}",
        inputs={"event_data": f"{namespace}"},
        outputs={"light_event_data": f"light_{namespace}"},
    )

def new_event_features_pipeline(namespace: str = "train", **kwargs) -> Pipeline:
    """
    """
    event_features_pipeline = pipeline(
        [
            node(
                func=time_diff_def,
                inputs="light_event_data",
                outputs="events",
                name="time_diffs",
            ),
        ]
    )

    return pipeline(
        pipe=event_features_pipeline,
        namespace=f"{namespace}",
        inputs={"light_event_data": f"light_{namespace}"},
        outputs={"events": f"events_{namespace}"},
    )

def new_qs_pipeline() -> Pipeline:
    return pipeline(
        [
            node(
                func=question_split,
                inputs="train_labels",
                outputs="labels_q",
                name="question_split",
            ),
        ]
    )


def new_split_pipeline() -> Pipeline:
    return pipeline(
        [
            node(
                func=jo_train_test_split,
                inputs=["events_train", "labels_q", "params:split_options"],
                outputs=["train_data", "labels_q_train", "test_data", "labels_q_test"],
                name="train_test_split",
            ),
        ]
    )