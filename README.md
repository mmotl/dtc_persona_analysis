# dtc_persona_analysis
customer persona analysis and segmentation mapping

<!--
![Bunny](./images/bunny.png)
-->

## Problem Statement  
A company got their customer data clustered and uses this for the creation of personae used in marketing.
Newly acquired customers must be assigned to the most fitting cluster.

## Approach
Requirements are:
Select a dataset that you're interested in (see Datasets)
Train a model on that dataset tracking your experiments
Create a model training pipeline
Deploy the model in batch, web service or streaming
Monitor the performance of your model
Follow the best practices

- created mock data / clustering
- found best k for kmeans clustering with mlflow experiment tracking
- 

the data is anonymized based on a real-world scenario from a former market research project


good practices considered:
- pr-commit webhooks are used to check for large files and private keys not being commited
- 

- outlines are used in the jupyter notebooks for easier navigation


future steps:
- consider timezones in date creation