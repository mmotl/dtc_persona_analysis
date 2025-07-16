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

import logging
logging.getLogger("mlflow").setLevel(logging.ERROR) # Suppress the MLflow warning - It only shows warning below the ERROR level.


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
    # mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment(experiment_name)

    # Enable scikit-learn autologging
    mlflow.sklearn.autolog()

    X = data

    # Experiment tracking

    with mlflow.start_run() as parent_run:
    # Iterate over the range of clusters
        for clusters in tqdm(range(2, 11)):
            print('iteration')
            
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
                mlflow.set_tag("run_purpose", "pipeline test")

    return None

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
