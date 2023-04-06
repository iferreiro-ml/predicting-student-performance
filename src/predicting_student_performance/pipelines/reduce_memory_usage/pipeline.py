"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node, pipeline

from ...nodes.reduce_memory_usage import reduce_memory_usage

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=reduce_memory_usage,
                inputs="train",
                outputs="light_train",
                name="reduce_train_mem_usage_node",
            ),
            node(
                func=reduce_memory_usage,
                inputs="test",
                outputs="light_test",
                name="reduce_test_mem_usage_node",
            ),
        ]
    )
