### Problem Statement
1. Background & context  
A key client has segmented its customer base using a cluster analysis performed by a third-party provider. These clusters are the foundation of their core marketing personas (e.g., "Sustainable Steve: The Forward-Thinking Business Leader" or "Eco-Conscious Haley: The Affluent, Sustainable Lifestyle Adopter") based on the mean of their demographic features. The mathematical definition for each persona is provided by a specific cluster centroid in a multi-dimensional feature space.

2. Core challenge  
The client has tasked us with building a system to classify new participants from our ongoing market research surveys into their pre-existing persona framework. The challenge is not to recreate the clustering, but to operationalize the labelling of new data points against the static, pre-defined cluster centroids provided by the original vendor.

3. Project objectives  
- Primary objective: To develop a robust and automated classification model that assigns new survey participants to the most appropriate marketing persona. The model's logic is based on calculating the proximity of a new data point to the provided persona centroids.
- Secondary objective: To implement a data monitoring system that tracks the statistical distribution of incoming survey data over time. This system will detect "data drift" and trigger a model re-training and deployment if the characteristics of new participants deviate significantly from the established persona definitions.  
*In real production ofc., a need for model retraining should not instantly re-train and deploy a model - this is just a technical showcase in this project. It should more trigger an alert to let decision makers re-evaluate the personas themselves.*

4. Data  
Core project assets we got provided (*in this project, since the original data is confidential, re-created with artificial data)*:
- Feature list: We have the definitive list of features (x1, x2, ..., x10) that define the persona space. These features will be incorporated into our survey instruments.
- Persona cluster centroids: We have received the numerical centroid for each persona. A centroid is a vector representing the mathematical average of all data points within a cluster, effectively serving as the "perfect example" or ideal center for that persona.  
*In this project, this is my ground truth for building new artificial data to be labelled.* 
