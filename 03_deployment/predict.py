import pandas as pd
from google.cloud import storage
import pickle
import io

import warnings
warnings.filterwarnings('ignore')

project_id = "tough-processor-312510"
storage_client = storage.Client(project=project_id)

# Get the bucket object
bucket = storage_client.bucket("mmotl_mlflow_artifacts")

# Path to the model file in the bucket
blob = bucket.blob("5/ba49d88bf2224b13a4643ac0104f12ad/artifacts/model/model.pkl")

# Download the model file as bytes
model_bytes = blob.download_as_bytes()

# Load the model using pickle
with io.BytesIO(model_bytes) as f:
    model = pickle.load(f)

def predict_labels(features):
    """
    Predict cluster labels for the input data X using the loaded KMeans model.
    It accepts either a list or a DataFrame as input and returns the predicted cluster labels.

    Parameters:
        X (array-like): Input data for prediction.

    Returns:
        array: Predicted cluster labels.
    """
    return model.predict(features)

if __name__ == "__main__":

    # Predict labels for the sample data
    predicted_labels = predict_labels(features)
    print("predicted labels:", predicted_labels)