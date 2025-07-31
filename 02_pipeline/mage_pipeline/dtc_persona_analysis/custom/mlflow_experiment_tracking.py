if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import mlflow
import mlflow.pyfunc

from tqdm import tqdm

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import requests
import sys
import os

import logging
# deactivated for debugging reasons
# logging.getLogger("mlflow").setLevel(logging.ERROR) # Suppress the MLflow warning - It only shows warning below the ERROR level.


@custom
def transform_custom(data, *args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    # Set up MLflow tracking
    # TO BE parametrized
    experiment_name = "dtc_persona_analysis"
    model_name = "dtc_persona_clustering_model"
    path = "../data/test_ref.csv" 

    mlflow.set_tracking_uri("http://mlflow_server:5000")
    print(f"MLflow tracking URI has been successfully set to: {mlflow.get_tracking_uri()}")
    
    # mlflow.set_tracking_uri("sqlite:///mlflow.db") # for local
    mlflow.set_experiment(experiment_name)

    # Enable scikit-learn autologging
    mlflow.sklearn.autolog()

    # Toggle here based on what model you want to create
#    X = data['reference']
    X = data['current']

    # Experiment tracking

    with mlflow.start_run() as parent_run:
    # Iterate over the range of clusters
        for clusters in tqdm(range(2, 11)):
            
            # Start a new MLflow run for each cluster count
            with mlflow.start_run(nested=True): #run_name=f"kmeans_basic_k={C}"):

                # Log the input data   
                mlflow.log_param("input_data_shape", X.shape)
                mlflow.log_param("input_data_columns", list(X.columns))

                # Instantiate your model
                # MLflow will capture these parameters automatically
                model = KMeans(n_clusters=clusters, n_init=10)#, random_state=42)
                
                # Fit the model
                # MLflow intercepts this .fit() call to log metrics and artifacts
                model.fit(X)

                # inertia is the sum of squared distances to the nearest cluster center
                # It is a measure of how tightly the clusters are packed
                # Lower inertia means better clustering
                mlflow.log_metric("inertia", model.inertia_)

                # Log silhouette score, which measures how similar an object is to its own cluster compared to other clusters
                # A higher silhouette score indicates better-defined clusters 
                silhouette = silhouette_score(X, model.fit_predict(X))
                mlflow.log_metric("silhouette", silhouette)

                # Log the ratio of silhouette score to inertia
                # This ratio can help assess the quality of clustering relative to the compactness of clusters
                score = silhouette * 1000 / model.inertia_
                mlflow.log_metric("silhouette_inertia_ratio", score)

                # Log the number of clusters
                mlflow.log_param("n_clusters", clusters)

                # Log the model itself
                mlflow.set_tag("run_purpose", "experiment from pipeline")
        
        experiment = mlflow.get_experiment_by_name(experiment_name)
        runs = mlflow.search_runs(
                                experiment_ids=[experiment.experiment_id],
                                order_by=["metrics.silhouette_inertia_ratio DESC"],
                                max_results=1
                                )
        best_run = runs.iloc[0]
    
    token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    message = os.environ.get('MESSAGE_DRIFT')

    
    # args: The output from any upstream parent blocks (if applicable)

    # The URL for the sendMessage method of the Telegram Bot API
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # The payload to be sent in the request
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'  # Optional: for message formatting (e.g., *bold*, _italic_)
    }

    try:
        # Send the request
        response = requests.post(url, data=payload)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        print("Message sent successfully!")
    #    return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
    #    return None

    return best_run.run_id # Return the ID of the best run

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
