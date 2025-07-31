# Clustering Metrics and Data Drift Monitoring

*Advanced techniques for evaluating clustering quality and monitoring data drift in unsupervised learning*

## Overview

This document explains two critical aspects of my clustering-based persona analysis system:

1. **Silhouette-Inertia-Ratio**: A custom metric for evaluating clustering quality
2. **Data Drift Monitoring**: How I monitor distribution changes in clustering problems

## Silhouette-Inertia-Ratio: A custom clustering metric

### The problem with traditional clustering evaluation

When working with k-means clustering, I face a fundamental challenge: **how do I determine the optimal number of clusters?** Traditional metrics have limitations:

- **Inertia alone**: Always decreases with more clusters (even meaningless ones)
- **Silhouette score alone**: May not capture cluster compactness
- **Elbow method**: Subjective and often unclear

### My solution: silhouette-inertia-ratio

I developed a custom metric that combines two complementary clustering quality measures - you can find this as logged metric in mlflow:

```python
silhouette_inertia_ratio = (silhouette_score * 1000) / model.inertia_
```

### Mathematical foundation
#### 1. Silhouette score (separation quality)
The silhouette score measures how similar a data point is to its own cluster compared to neighboring clusters:

```
silhouette(i) = (b(i) - a(i)) / max(a(i), b(i))
```

Where:
- `a(i)`: Average distance from point i to all other points in its cluster
- `b(i)`: Minimum average distance from point i to points in other clusters

**Range**: -1 to +1
- **+1**: Perfect separation (point is far from other clusters)
- **0**: Point is on cluster boundary
- **-1**: Point likely assigned to wrong cluster

#### 2. Inertia (compactness quality)
Inertia is the sum of squared distances from each point to its cluster centroid:

```
inertia = Σ(distance(point_i, centroid_k)²)
```

**Characteristics**:
- **Lower values**: Tighter, more compact clusters
- **Always decreases**: As number of clusters increases
- **No upper bound**: Can be very large numbers

### Why the ratio works

The silhouette-inertia-ratio creates a balanced evaluation by:

1. **Rewarding separation**: Higher silhouette scores increase the ratio
2. **Rewarding compactness**: Lower inertia values increase the ratio
3. **Penalizing over-clustering**: Models with too many clusters get lower ratios
4. **Finding the sweet spot**: Optimal balance between separation and compactness. In mlflow, the registered model with the best score is considered the best run and hence promoted/deployed.

### Implementation in mlflow

```python
def experiment_tracking(X, k_min, k_max):
    """Run K-Means experiments with custom metric tracking."""
    with mlflow.start_run() as parent_run:
        for clusters in range(k_min, k_max + 1):
            with mlflow.start_run(nested=True):
                # Train K-Means model
                model = KMeans(n_clusters=clusters, n_init=10)
                model.fit(X)
                
                # Calculate metrics
                silhouette = silhouette_score(X, model.fit_predict(X))
                inertia = model.inertia_
                
                # Custom ratio metric
                score = silhouette * 1000 / inertia
                
                # Log to MLflow
                mlflow.log_metric("silhouette", silhouette)
                mlflow.log_metric("inertia", inertia)
                mlflow.log_metric("silhouette_inertia_ratio", score)
                mlflow.log_param("n_clusters", clusters)
```

### Scaling factor (×1000)

The multiplication by 1000 is purely for **readability**:
- Silhouette scores: ~0.1 to 0.8
- Inertia values: ~1000 to 10000
- Without scaling: ratio = 0.0001 (hard to read)
- With scaling: ratio = 0.1 (much clearer)

## Data drift monitoring in clustering context

### The unique challenge of clustering drift

Unlike supervised learning, clustering problems present unique challenges for drift detection:

1. **No ground truth labels**: I can't measure prediction accuracy drift
2. **Feature distribution changes**: May indicate new customer segments
3. **Cluster centroid shifts**: Existing personas may no longer be relevant
4. **New cluster emergence**: New customer types may appear

### My drift detection strategy

I use **evidently ai** to monitor data distribution changes that could affect clustering quality:

#### 1. Statistical distribution monitoring

```python
def evaluate_condition(data):
    """Evaluate data drift between reference and current datasets."""
    reference_data = data["reference"]
    current_data = data["current"]
    
    # Create drift detection report
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(reference_data=reference_data, current_data=current_data)
    
    # Get drift detection result
    drift_result = report.as_dict()["metrics"][0]["result"]["dataset_drift"]
    
    if drift_result:
        print("Significant data drift detected")
    else:
        print("No significant data drift detected")
    
    return drift_result
```

#### 2. What I monitor

**Feature distribution changes by EvidentlyAI column drift metrics**:
- Statistical tests on each feature (x1-x10)
- afaik: Kolmogorov-smirnov tests for distribution shifts

#### 3. Drift detection pipeline

```
[New data arrives] → [Load reference data] → [Evidently analysis] → [Drift decision]
                                                                         ↓
                                               [Retrain model] ← (if drift detected)
```

### Real-world drift scenarios

#### Scenario 1: Seasonal customer behavior changes
- **Trigger**: March data shows different feature distributions
- **Impact**: Existing personas may not capture new patterns
- **Action**: Retrain clustering model with updated data

#### Scenario 2: Market expansion
- **Trigger**: New customer segments with different characteristics
- **Impact**: Current centroids may not represent new segments
- **Action**: Increase cluster count or retrain with expanded dataset

#### Scenario 3: Feature engineering changes
- **Trigger**: Survey questions or data collection methods change
- **Impact**: Feature space shifts, making old centroids irrelevant
- **Action**: Retrain model with new feature definitions

### Drift thresholds and decision making

EvidentlyAI uses **statistical significance** rather than arbitrary thresholds:

- **p-value < 0.05**: Significant drift detected
- **Multiple features affected**: Higher confidence in drift

## Integration with MLOps pipeline

### Automated retraining workflow

1. **Data ingestion**: New monthly customer data arrives
2. **Drift detection**: Compare with january reference data
3. **Conditional branching**: 
   - **No drift**: Continue with existing model
   - **Drift detected**: Trigger model retraining and send alert
4. **Model evaluation**: Use silhouette-inertia-ratio to select best model
5. **Model registration**: Log new model in mlflow registry
6. **Model promotion**: Promote best model to production
7. **Deployment**: Update serving infrastructure
