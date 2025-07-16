import mlflow
import mlflow.pyfunc

from model_register_best_run import find_best_run

import logging
logging.getLogger("mlflow").setLevel(logging.ERROR) # Suppress the MLflow warning - It only shows warning below the ERROR level.

# Set up MLflow tracking
# TO BE parametrized
experiment_name = "dtc_persona_analysis"
model_name = "dtc_persona_clustering_model"

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment(experiment_name)

def load_model():

    best_run_id = find_best_run(experiment_name).run_id
    print(f"Best run ID: {best_run_id}")
    # This will register the model with the best silhouette_inertia_ratio
    model_uri = f"runs:/{best_run_id}/model"
    print(f"Model URI: {model_uri}")

    # Define the Model URI
    model_version = 2
    model_uri = f"models:/{model_name}/{model_version}"

    print(f"Loading model from: {model_uri}")

    # loading the model using mlflow.sklearn.load_model to ensure compatibility with scikit-learn attributes
    try:
        loaded_model = mlflow.sklearn.load_model(model_uri)
        print("Model loaded successfully!")
        return loaded_model
    except Exception as e:
        print(f"Error loading model: {e}")
        # Exit if model fails to load
        exit()



if __name__ == "__main__":
    load_model()