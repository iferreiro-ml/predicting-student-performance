"""
This is a boilerplate pipeline 'modelling'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import upsample_minority_class, df_to_numpy, create_scaler, train_clf, scale, classify

def new_train_pipeline(**kwargs) -> Pipeline:
    train_pipeline = pipeline(
        [
            node(
                func=upsample_minority_class,
                inputs=["features_q", "labels_q", "params:upsampling_seed"],
                outputs=["upsampled_features_q", "upsampled_labels_q"],
                name="upsampling_pipeline",
            ),
            node(
                func=df_to_numpy,
                inputs="upsampled_features_q",
                outputs="unscaled_X",
                name="features_train_to_numpy",
            ),
            node(
                func=df_to_numpy,
                inputs="upsampled_labels_q",
                outputs="y",
                name="labels_train_to_numpy",
            ),
            node(
                func=create_scaler,
                inputs="unscaled_X",
                outputs=["X", "scaler"],
                name="scale_train",
            ),
            node(
                func=train_clf,
                inputs=["X", "y"],
                outputs="clf",
                name="train_classifier",
            ),
        ]
    )

    return pipeline(
        pipe=train_pipeline,
        parameters="params:upsampling_seed",
        outputs=["scaler", "clf"],
        namespace="train"
    )  + new_modular_classify_pipeline("train")


def new_classify_pipeline(dataset = "test", **kwargs) -> Pipeline:
    predict_prep_pipeline = pipeline(
        [
            node(
                func=df_to_numpy,
                inputs="features_q",
                outputs="unscaled_X",
                name="features_test_to_numpy",
            ),
            node(
                func=df_to_numpy,
                inputs="labels_q",
                outputs="y",
                name="labels_test_to_numpy",
            ),
            node(
                func=scale,
                inputs=["unscaled_X", "scaler"],
                outputs="X",
                name="scale_test",
            ),
        ]
    )

    return pipeline(
        pipe=predict_prep_pipeline,
        inputs="scaler",
        namespace=dataset,
    ) + new_modular_classify_pipeline("test")


def new_modular_classify_pipeline (dataset = "test", **kwargs) -> Pipeline:
    predict_pipeline = pipeline(
        [
            node(
                func=classify,
                inputs=["X", "clf"],
                outputs="y_pred",
            ),
        ]
    )

    return pipeline(
        pipe=predict_pipeline,
        inputs={"X": f"{dataset}.X", "clf": "clf"},
        outputs = {"y_pred": f"{dataset}.y_pred"},
        namespace=f"{dataset}_predict",
    )