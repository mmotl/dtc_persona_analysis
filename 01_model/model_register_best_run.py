import mlflow
import mlflow.pyfunc

import logging
logging.getLogger("mlflow").setLevel(logging.ERROR) # Suppress the MLflow warning - It only shows warning below the ERROR level.

# Set up MLflow tracking
# TO BE parametrized
experiment_name = "dtc_persona_analysis"
model_name = "dtc_persona_clustering_model"

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment(experiment_name)



# Find the best run based on the silhouette_inertia_ratio metric and return the run ID.
def find_best_run(experiment_name):
    '''Find the best run based on the silhouette_inertia_ratio metric.
    Returns:
        best run object
    '''
    # Search for runs in the current experiment to find the best model, sorted by the main score "silhouette_inertia_ratio" descending
    experiment = mlflow.get_experiment_by_name(experiment_name)
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.silhouette_inertia_ratio DESC"],
        max_results=1
    )

    best_run = runs.iloc[0]

    if not runs.empty:
        print("Best run ID:", best_run.run_id)
        print("Best silhouette_inertia_ratio:", best_run["metrics.silhouette_inertia_ratio"])
        print("Count of clusters:", best_run["params.n_clusters"])
        return best_run # Return the ID of the best run
    else:
        raise ValueError("No runs found in the experiment.")


def register_best_run(experiment_name, model_name):

    # Register the best run's model in the MLflow Model Registry.
    best_run_id = find_best_run(experiment_name).run_id
    print(f"Best run ID: {best_run_id}")
    # This will register the model with the best silhouette_inertia_ratio
    model_uri = f"runs:/{best_run_id}/model"
    mlflow.register_model(model_uri, model_name)

    return model_uri