import sys
import pandas as pd
from sklearn.datasets import make_blobs

'''
This script generates synthetic data using the make_blobs function from sklearn.
It creates a DataFrame with 10 features and saves it to a CSV file.
Usage:
    python create_data.py <n> <C> <cluster_std> <RSEED> [<filename>]
where:
    n: Number of samples
    C: Number of clusters
    cluster_std: Standard deviation of clusters
    RSEED: Random seed for reproducibility
    filename: Output filename
    '''

n = int(sys.argv[1])  # Number of samples
C = int(sys.argv[2])  # Number of clusters
cluster_std = float(sys.argv[3])  # Standard deviation of clusters
RSEED = int(sys.argv[4])  # Random seed for reproducibility
filename = sys.argv[5] if len(sys.argv) > 0 else 'data.csv'  # Output filename

def create_data(n, C, cluster_std, RSEED):
    '''Generate synthetic data using make_blobs and return a DataFrame.
    Args:
        n (int): Number of samples.
        C (int): Number of clusters.
        cluster_std (float): Standard deviation of clusters.
        RSEED (int): Random seed for reproducibility.
    Returns:
        pd.DataFrame: DataFrame containing the generated data.'''
    X, y = make_blobs(n_samples=n, 
                      n_features=10, 
                      centers=C, 
                      cluster_std=cluster_std, 
                      center_box=(-10.0, 10.0), 
                      random_state=RSEED)
    df = pd.DataFrame(X, columns=['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'])
    
    return df

def save_data(df, filename=filename):
    '''Save the DataFrame to a CSV file.
    Args:
        df (pd.DataFrame): DataFrame to save.
        filename (str): Name of the output CSV file.
    Returns:
        str: The filename where the data is saved.'''
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    return filename


if __name__ == "__main__":
    '''Main function to create and save the data.'''
    df = create_data(n, C, cluster_std, RSEED)
    filename = save_data(df)
    print(f"Dataframe shape: {df.shape}")