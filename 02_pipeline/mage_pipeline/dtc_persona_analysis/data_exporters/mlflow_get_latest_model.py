if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


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
    import mlflow
    from mlflow.tracking import MlflowClient

    # Set the tracking URI to point to your MLflow server
    # This should match the address of your mlflow_server container
    mlflow.set_tracking_uri("http://mlflow_server:5000")

    # Initialize the MLflow client
    client = MlflowClient()

    # Define the name of the registered model you want to get the latest version for
    model_name = "dtc_persona_clustering_model"

    try:
        # Get the latest versions of the registered model
        latest_versions = client.get_latest_versions(name=model_name, stages=["None"])

        # The result is a list, so we get the first element
        if latest_versions:
            latest_version = latest_versions[0]
            print(f"Latest version for model '{model_name}':")
            print(f"  Version: {latest_version.version}")
            print(f"  Run ID: {latest_version.run_id}")
            print(f"  Stage: {latest_version.current_stage}")
            print(f"  Source: {latest_version.source}")
            print(f"  Creation Timestamp: {latest_version.creation_timestamp}")

            # You can also load the model directly using this information
            # loaded_model = mlflow.pyfunc.load_model(f"models:/{model_name}/{latest_version.version}")
            # print("\nModel loaded successfully.")

        else:
            print(f"No versions found for model '{model_name}'.")

    except mlflow.exceptions.RestException as e:
        print(f"Error communicating with MLflow server: {e}")
        print(f"Please ensure the model name '{model_name}' is correct and the MLflow server is running.")

    return latest_version.version