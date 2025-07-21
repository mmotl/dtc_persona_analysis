import sys
import pandas as pd
from sklearn.datasets import make_blobs

"""
This script generates synthetic data using the make_blobs function from sklearn.
It creates a DataFrame with 10 features and saves it to a CSV file.
Usage:
    python create_data.py <n> <C> <cluster_std> <RSEED> [<filename>]
where:
    n: Number of samples
    cluster_std: Standard deviation of clusters
    RSEED: Random seed for reproducibility
    filename: Output filename
    not used: C: Number of clusters, centroids are initialized in the code
    """

n = int(sys.argv[1])  # Number of samples (500 in the original code)
cluster_std = float(
    sys.argv[2]
)  # Standard deviation of clusters (2 in the original code)
RSEED = int(sys.argv[3])  # Random seed for reproducibility
month = int(sys.argv[4])  # Month for the date column (default is June)
filename = sys.argv[5] if len(sys.argv) > 0 else "data.csv"  # Output filename
# C = int(sys.argv[5])  # Number of clusters (3 in the original code)

# initialization of centroids
# These centroids are used to generate the synthetic data.
centroids = [
    [
        -2.50919762,
        9.01428613,
        4.63987884,
        1.97316968,
        -6.87962719,
        -6.88010959,
        -8.83832776,
        7.32352292,
        2.02230023,
        4.16145156,
    ],
    [
        -9.58831011,
        9.39819704,
        6.64885282,
        -5.75321779,
        -6.36350066,
        -6.3319098,
        -3.91515514,
        0.49512863,
        -1.36109963,
        -4.1754172,
    ],
    [
        2.23705789,
        -7.21012279,
        -4.15710703,
        -2.67276313,
        -0.87860032,
        5.70351923,
        -6.00652436,
        0.28468877,
        1.84829138,
        -9.07099175,
    ],
]


def create_data(n, cluster_std, RSEED, month, C):
    """Generate synthetic data using make_blobs and return a DataFrame.
    Args:
        n (int): Number of samples.
        C (int): Number of clusters.
        cluster_std (float): Standard deviation of clusters.
        RSEED (int): Random seed for reproducibility.
    Returns:
        pd.DataFrame: DataFrame containing the generated data."""
    X, y = make_blobs(
        n_samples=n,
        n_features=10,
        centers=C,
        cluster_std=cluster_std,
        center_box=(-10.0, 10.0),
        random_state=RSEED,
    )
    df = pd.DataFrame(
        X, columns=["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"]
    )
    df.insert(0, "date", pd.to_datetime(f"2025-{month:02d}-01"))

    return df


def save_data(df, filename=filename):
    """Save the DataFrame to a CSV file.
    Args:
        df (pd.DataFrame): DataFrame to save.
        filename (str): Name of the output CSV file.
    Returns:
        str: The filename where the data is saved."""
    df.to_csv(f"../data/{filename}", index=False)
    print(f"Data saved to {filename}")
    return filename


if __name__ == "__main__":
    """Main function to create and save the data."""
    df = create_data(n, cluster_std, RSEED, month, C=centroids)
    filename = save_data(df)

    print(f"Dataframe shape: {df.shape}")
