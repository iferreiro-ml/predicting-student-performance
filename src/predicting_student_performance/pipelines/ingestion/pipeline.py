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

def new_rmu_pipeline(dataset: str = "train") -> Pipeline:
    """rmu stands for "reduce memory usage"
    This pipeline creates a modular instance that can be applied to
    any event_data DataFrame to type it, thus reducing its memory usage.
    The name of the event_data DataFrame has to be input in the dataset argument 
    """

    rmu_pipeline = pipeline(
        [
            node(
                func=reduce_memory_usage,
                inputs="event_data",
                outputs="light_event_data",
                name=f"{dataset}_rmu_node",
            ),
        ]
    )

    return pipeline(
        pipe=rmu_pipeline,
        inputs={"event_data": f"{dataset}"},
        outputs={"light_event_data": f"light_{dataset}"},
        namespace=f"{dataset}_ingestion"
    )

def new_event_features_pipeline(dataset: str = "train", **kwargs) -> Pipeline:
    """
    """
    event_features_pipeline = pipeline(
        [
            node(
                func=time_diff_def,
                inputs="light_event_data",
                outputs="events",
                name=f"{dataset}_time_diffs",
            ),
        ]
    )

    return pipeline(
        pipe=event_features_pipeline,
        namespace=f"{dataset}_ingestion",
        inputs={"light_event_data": f"light_{dataset}"},
        outputs={"events": f"events_{dataset}"},
    )

def new_qs_pipeline() -> Pipeline:
    question_split_pipeline = pipeline(
        [
            node(
                func=question_split,
                inputs="train_labels",
                outputs="labels_q",
                name="question_split",
            ),
        ]
    )

    return pipeline(
        pipe=question_split_pipeline,
        inputs="train_labels",
        outputs="labels_q",
        namespace="train_ingestion"
    )


def new_split_pipeline() -> Pipeline:
    split_pipeline = pipeline(
        [
            node(
                func=jo_train_test_split,
                inputs=["events_train", "labels_q", "params:split_options"],
                outputs=["train.events_data", "train.labels_q", "test.events_data", "test.labels_q"],
                name="train_test_split",
            ),
        ],
    )
    return pipeline(
        pipe=split_pipeline,
        inputs=["events_train", "labels_q"],
        parameters="params:split_options",
        outputs=["train.events_data", "train.labels_q", "test.events_data", "test.labels_q"],
        namespace="train_ingestion"
    )