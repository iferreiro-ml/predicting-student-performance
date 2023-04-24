"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from predicting_student_performance.pipelines import ingestion as ing
from predicting_student_performance.pipelines import feature_engineering as fe
from predicting_student_performance.pipelines import modelling as mod

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """

    train_rmu_pipeline = ing.new_rmu_pipeline("train")
    test_rmu_pipeline = ing.new_rmu_pipeline("test")
    train_event_features_pipeline = ing.new_event_features_pipeline("train")
    question_split_pipeline = ing.new_qs_pipeline()
    train_test_split_pipeline = ing.new_split_pipeline()
    train_fe_pipeline = fe.create_pipeline("train")
    test_fe_pipeline = fe.create_pipeline("test")
    upsampling_pipeline = mod.create_upsampling_pipeline()

    return {
        "rmu_all": train_rmu_pipeline + test_rmu_pipeline,
        "ing_without_rmu": train_event_features_pipeline + question_split_pipeline + train_test_split_pipeline,
        "full_ingestion": train_rmu_pipeline + test_rmu_pipeline + train_event_features_pipeline + question_split_pipeline + train_test_split_pipeline,
        "__default__": train_test_split_pipeline,
        "train_e2e": train_event_features_pipeline + question_split_pipeline + train_test_split_pipeline + train_fe_pipeline + test_fe_pipeline + upsampling_pipeline,
        "modelling": upsampling_pipeline,
    }
