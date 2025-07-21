import pandas as pd
from google.cloud import storage
import pickle
import io

from flask import Flask, request, jsonify

import warnings
warnings.filterwarnings('ignore')

# Initialize a storage client
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


app = Flask('label_predictor')

@app.route('/predict', methods=['POST'])
def predict_labels():
    """
    """
    # 1. Get the data from the incoming request
    json_data = request.get_json()
    print("Received data:", json_data)

    # 2. Convert it to a DataFrame
    features = pd.DataFrame(json_data)
    print("Converted DataFrame:", features)
        # Define the correct feature names
    feature_names = [
        'x1', 'x2', 'x3', 'x4', 'x5', 
        'x6', 'x7', 'x8', 'x9', 'x10'
    ]

    # Rename the columns from '0', '1', ... to 'x1', 'x2', ...
    features.columns = feature_names

    predictions_nparray = model.predict(features)
    predictions_list = predictions_nparray.tolist()
    # print("Predictions:", predictions_list)

    result = {
        'labels': predictions_list
    }

    return jsonify(result)

if __name__ == "__main__":

    # # Predict labels for the sample data
    # model = get_model()
    # predicted_labels = predict_labels(features)
    # print("predicted labels:", predicted_labels)

    app.run(debug=True, host='0.0.0.0', port=9696)