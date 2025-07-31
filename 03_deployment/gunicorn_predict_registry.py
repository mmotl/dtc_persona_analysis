import pandas as pd
import mlflow
import sys
import logging
from flask import Flask, request, jsonify

# Configure logging for Gunicorn
logging.basicConfig(level=logging.INFO)

# Global model variable
model = None

def load_model():
    """
    Load the MLflow model from the model registry and assign to the global 'model' variable.
    Exits the process if loading fails.
    """
    global model
    MLFLOW_TRACKING_URI = "http://localhost:5050"
    MODEL_NAME = "dtc_persona_clustering_model"
    MODEL_STAGE = "Production"
    MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
    model = None
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        logging.info(f"Connecting to MLflow Tracking Server at: {MLFLOW_TRACKING_URI}")
        logging.info(f"Loading model '{MODEL_NAME}' from stage '{MODEL_STAGE}'...")
        model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)
    except mlflow.exceptions.RestException as e:
        logging.error("Failed to load the model due to an MLflow REST API error.")
        logging.error(f"Check if MLflow server is running at '{MLFLOW_TRACKING_URI}', if model '{MODEL_NAME}' exists, and if it has a version in stage '{MODEL_STAGE}'.")
        logging.error(f"Original Error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error occurred while loading the model: {e}")
        sys.exit(1)
    else:
        logging.info("Model loaded successfully!")
        if hasattr(model, "metadata"):
            logging.info(f"Model Signature: {model.metadata.signature}")


app = Flask("label_predictor")

# Load model at startup (for Gunicorn --preload efficiency)
load_model()


@app.route("/predict", methods=["POST"])
def predict_labels():
    """
    Predict persona labels for input features (expects JSON array of feature dicts).
    Returns: JSON with predicted labels.
    """
    if model is None:
        return (
            jsonify({"error": "Model is not available. Check server logs for details."}),
            500,
        )
    json_data = request.get_json()
    features = pd.DataFrame(json_data)
    feature_names = [f"x{i}" for i in range(1, 11)]
    features.columns = feature_names
    predictions_nparray = model.predict(features)
    result = {"labels": predictions_nparray.tolist()}
    return jsonify(result)

# For local debugging only (not used by Gunicorn)
# if __name__ == "__main__":
