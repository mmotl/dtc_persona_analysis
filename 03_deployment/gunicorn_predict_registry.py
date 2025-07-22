import pandas as pd
# from google.cloud import storage
import mlflow
import sys
# import io
# import os
import logging
from flask import Flask, request, jsonify

# Configure logging so messages are visible in your gunicorn.log file
logging.basicConfig(level=logging.INFO)

# --- Global model variable ---
# Define a variable in the global scope that will hold our model.
model = None

def load_model():
    """
    Loads the model from GCS and populates the global 'model' variable.
    This function will be called once when the script is loaded.
    """
    global model
   

# --- Configuration ---
    MLFLOW_TRACKING_URI = "http://localhost:5050"
    MODEL_NAME = "dtc_persona_clustering_model"
    MODEL_STAGE = "Production"
    MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_STAGE}"

    # Initialize a variable to hold the model
    model = None

    try:
        # --- Step 1: Set the tracking URI ---
        # This tells the MLflow client where to send requests.
        print(f"Connecting to MLflow Tracking Server at: {MLFLOW_TRACKING_URI}")
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

        # --- Step 2: Load the model ---
        # This is the primary operation that might fail if the server is unreachable
        # or the model/stage does not exist.
        print(f"Loading model '{MODEL_NAME}' from stage '{MODEL_STAGE}'...")
        model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)

    # Catch specific MLflow exceptions for better error messages
    except mlflow.exceptions.RestException as e:
        print("\n--- MLFLOW ERROR ---")
        print(f"Failed to load the model due to an MLflow REST API error.")
        print("This commonly happens if:")
        print(f"  1. The MLflow server is not running or accessible at '{MLFLOW_TRACKING_URI}'.")
        print(f"  2. The model named '{MODEL_NAME}' does not exist in the registry.")
        print(f"  3. The model does not have a version assigned to the '{MODEL_STAGE}' stage.")
        print(f"\nOriginal Error: {e}")
        # Exit the script with an error code, as the application cannot continue.
        sys.exit(1)

    # Catch any other unexpected exceptions during the process
    except Exception as e:
        print(f"\n--- AN UNEXPECTED ERROR OCCURRED ---")
        print(f"An error occurred while trying to load the model: {e}")
        sys.exit(1)

    # The 'else' block runs only if the 'try' block completes successfully
    else:
        print("\n✅ Model loaded successfully!")
        # You can now use the 'model' object for predictions.
        # For example, print its metadata if available.
        if hasattr(model, 'metadata'):
            print(f"Model Signature: {model.metadata.signature}")

# --- Flask App Definition ---
app = Flask("label_predictor")

# --- Model Loading ---
# This is the key change. We call load_model() directly in the script's global scope.
# When Gunicorn runs with '--preload', this function executes exactly once in
# the master process. The loaded 'model' variable is then inherited by all the
# worker processes, which is highly efficient.
load_model()


@app.route("/predict", methods=["POST"])
def predict_labels():
    """
    Handles prediction requests.
    """
    # A check to ensure the model was loaded correctly during startup.
    if model is None:
        return jsonify({"error": "Model is not available. Check server logs for details."}), 500

    json_data = request.get_json()
    features = pd.DataFrame(json_data)

    feature_names = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"]
    features.columns = feature_names

    predictions_nparray = model.predict(features)
    result = {"labels": predictions_nparray.tolist()}

    return jsonify(result)

# This block is only for local debugging (e.g., 'python gunicorn

# This block is for local debugging only, Gunicorn will not run this.
# if __name__ == "__main__":
    