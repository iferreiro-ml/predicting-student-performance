"""
This is a boilerplate pipeline 'reporting'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import overall_performance, question_performance, track_params


def create_pipeline(dataset = "test", **kwargs) -> Pipeline:
    report_pipeline = pipeline(
        [
            node(
                func=overall_performance,
                inputs=["y", "y_pred"],
                outputs=["overall_metrics", "op_table"],
                name="overall_performance_reporting",
            ),
            node(
                func=question_performance,
                inputs=["y", "y_pred"],
                outputs=["question_metrics", "qp_table"],
                name="question_performance_reporting",
            )
        ]
    )

    return pipeline(
        pipe=report_pipeline,
        namespace = f"{dataset}_report",
        inputs = dict(zip(
            [x for x in report_pipeline.inputs()],
            [f"{dataset}.{x}" for x in report_pipeline.inputs()])),
        outputs  = dict(zip(
            [x for x in report_pipeline.outputs()],
            [f"{dataset}.{x}" for x in report_pipeline.outputs()]))
    )

def new_param_track_pipeline() -> Pipeline:
    return pipeline(
        [
            node(
                func=track_params,
                inputs=["params:split_options", "params:upsampling_seed"],
                outputs="tracked_parameters",
                name="track_parameters",
            )
        ]
    )