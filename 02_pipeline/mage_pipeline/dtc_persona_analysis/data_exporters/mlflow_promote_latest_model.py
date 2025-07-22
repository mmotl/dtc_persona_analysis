if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import mlflow
from mlflow.tracking import MlflowClient

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    

    mlflow.set_tracking_uri("http://mlflow_server:5000")
    client = MlflowClient()
    model_name = "dtc_persona_clustering_model"

    # You've already found the latest version, let's say its version number is '19'
    latest_version_info = client.get_latest_versions(name=model_name, stages=["None"])[0]
    version_to_promote = latest_version_info.version

    print(f"Promoting version {version_to_promote} of model '{model_name}' to 'Production'.")

    # This is the key step:
    client.transition_model_version_stage(
        name=model_name,
        version=version_to_promote,
        stage="Production",
        archive_existing_versions=True # This will move any existing 'Production' model to 'Archived'
    )

    print("Promotion successful.")


