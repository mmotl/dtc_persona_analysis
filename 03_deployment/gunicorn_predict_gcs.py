import pandas as pd
from google.cloud import storage
import pickle
import io
import os
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
    try:
        project_id = "tough-processor-312510"
        bucket_name = "mmotl_mlflow_artifacts"
        blob_path = "5/ba49d88bf2224b13a4643ac0104f12ad/artifacts/model/model.pkl"

        logging.info("Initializing GCS client...")
        storage_client = storage.Client(project=project_id)

        logging.info(f"Downloading model from gs://{bucket_name}/{blob_path}")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        model_bytes = blob.download_as_bytes()

        logging.info("Loading model using pickle...")
        model = pickle.load(io.BytesIO(model_bytes))
        logging.info("✅ Model loaded successfully and is ready.")

    except Exception as e:
        # Log the full error to the console/log file to help with debugging.
        logging.error(f"❌ Failed to load model: {e}", exc_info=True)
        model = None

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
    