"""
This is a boilerplate pipeline 'modelling'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import upsample_minority_class, df_to_numpy, create_scaler, train_clf, classify

def create_train_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=upsample_minority_class,
                inputs=["features_q_train", "labels_q_train", "params:upsampling_seed"],
                outputs=["upsampled_features_q_train", "upsampled_labels_q_train"],
                name="upsampling_pipeline",
            ),
            node(
                func=df_to_numpy,
                inputs="upsampled_features_q_train",
                outputs="unscaled_X_train",
                name="features_train_to_numpy",
            ),
            node(
                func=df_to_numpy,
                inputs="upsampled_labels_q_train",
                outputs="y_train",
                name="labels_train_to_numpy",
            ),
            node(
                func=create_scaler,
                inputs="unscaled_X_train",
                outputs=["X_train", "scaler"],
                name="scale",
            ),
            node(
                func=train_clf,
                inputs=["X_train", "y_train"],
                outputs="clf",
                name="train_classifier",
            ),
        ]
    )

def create_predict_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=df_to_numpy,
                inputs="features_q_test",
                outputs="X_test",
                name="features_test_to_numpy",
            ),
            node(
                func=df_to_numpy,
                inputs="labels_q_test",
                outputs="y_test",
                name="labels_test_to_numpy",
            ),
            node(
                func=classify,
                inputs=["X_test", "clf"],
                outputs="y_pred",
                name="classify",
            ),
        ]
    )