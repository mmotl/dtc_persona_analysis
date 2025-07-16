import pandas as pd
import mlflow
import mlflow.pyfunc

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from tqdm import tqdm #Progress bar for loops

import logging
logging.getLogger("mlflow").setLevel(logging.ERROR) # Suppress the MLflow warning - It only shows warning below the ERROR level.



# Set up MLflow tracking
# TO BE parametrized
experiment_name = "dtc_persona_analysis"
model_name = "dtc_persona_clustering_model"
path = "../data/test_ref.csv" 

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment(experiment_name)

# Enable scikit-learn autologging
mlflow.sklearn.autolog()

# Load the dataset
def read_data(path):
    X = pd.read_csv(path)
    return X

# Experiment tracking function
def experiment_tracking(X, k_min, k_max):
    '''Run the experiment tracking for KMeans clustering.
    Args:
        X (pd.DataFrame): DataFrame containing the data to cluster.
    Returns:
        None'''
    with mlflow.start_run() as parent_run:
    # Iterate over the range of clusters
        for clusters in tqdm(range(k_min, k_max + 1)):
            
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
                mlflow.set_tag("run_purpose", "script test")

    return None


# Main execution
if __name__ == "__main__":
    # Read the data
    X = read_data(path)
    # Run the experiment tracking
    experiment_tracking(X, k_min=2, k_max=10)