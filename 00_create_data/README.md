## Building the Dataset
### Why Pre-Defined Centroids are Crucial for Mock Clustering Data

```
TL/DR:  
In this project, mock data is used.
- It is created with scikit-learn, creates so-called 'blobs', to gain a dataset with known metrics and which is suitable for clustering in first place.  
- a k-means algorithm is fit to the data.  
- the dataset then gets labeled by the k-means algorithm.
- from the models attributes, the centroids of the clusters (their center points) are extracted.
    - (this would be the real world scenario. With mock data, we can return the centroids during data generation directly.)
- these centroids are used to create additional data with slightly different metrics, but still same cluster locations.  
- imagine this as data about new customers: they might be a little different in age or income, but still they have specifications of customers within the defined deviations ... 
```
<!-- [Cluster Centroid Illustration](../images/cluster_centroid.png) -->


So, in short:  
When creating mock data for a clustering experiment, defining the cluster centroids beforehand using an initial labeling model is essential for a robust and insightful analysis. This approach provides a "ground truth" or a known correct answer, which is the cornerstone of effective algorithm evaluation.  
If there were no cluster centroids provided, the creation of mock data would be randomly initialised and the new data would most likely not be clustered meaningfully by an existing model.

Here's why this is a necessary step:

*   **Enables Controlled Evaluation:** By establishing the true center of each cluster, you create a controlled environment. This allows you to measure an algorithm's performance accurately using evaluation metrics. Without a ground truth, you can't objectively know how well the algorithm uncovered the underlying structure of the data.

*   **Allows for Realistic and Complex Scenarios:** An initial model lets you design challenging, real-world scenarios. You can strategically place centroids to create overlapping clusters, vary the density and size of the groups, or even form non-linear shapes. This tests the limits and flexibility of your clustering algorithms in a way that purely random data cannot.

*   **Guarantees Reproducibility:** Defining the centroids ensures that you can recreate the exact same dataset at any time. This is critical for validating your results, comparing different models fairly, and allowing others to reproduce your experiment.

*   **Aids in Algorithm Development and Testing:** Many algorithms, like K-means, are sensitive to their initial starting points. By using mock data with known centroids, you can fairly test how different initialization strategies perform and diagnose whether an algorithm is failing due to a poor start or a fundamental inability to handle the data's structure.