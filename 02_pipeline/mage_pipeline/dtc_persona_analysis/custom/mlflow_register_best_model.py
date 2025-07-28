if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import mlflow

@custom
def transform_custom(data, *args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    mlflow.set_tracking_uri("http://mlflow_server:5000")
    model_name = "dtc_persona_clustering_model"
    best_run_id = data

    # Register model
    # This will register the model with the best silhouette_inertia_ratio
    model_uri = f"runs:/{best_run_id}/model"
    mlflow.register_model(model_uri, model_name)

    return best_run_id


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
