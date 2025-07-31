## Evaluation criteria
This document is meant to help you with the evaluation,  
I'm using the original `DataTalksClub` [outline](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/07-project) to guide you through the project:

* Problem description
    * it's ofc up to you if you consider the problem well described
    * see the [main README.md](./README.md) for a detailed description and setup guideance,  
    * a [mock data / general modelling](00_create_data/README.md) in-depth description and thoughts here.
* Cloud
    * IaC tools (see [`05_iac/`](05_iac/)) are used to provision a `GCP storage bucket` as the `MLflow artifact store`.
    * the `MAGE pipeline` is containerized in a [Docker Compose](02_pipeline/mage_pipeline/docker-compose.yml) stack, yet running locally.
* Experiment tracking and model registry
    * both [experiment tracking](02_pipeline/mage_pipeline/dtc_persona_analysis/custom/mlflow_experiment_tracking.py) and [model registry](02_pipeline/mage_pipeline/dtc_persona_analysis/custom/mlflow_register_best_model.py) are used inside the 'MAGE pipeline'.
    * the model registry is set up as a containerized `Postgresql` database in [Docker Compose](02_pipeline/mage_pipeline/docker-compose.yml).
    * after model training, the best run is identified, the model gets [registered and promoted](02_pipeline/mage_pipeline/dtc_persona_analysis/data_exporters/mlflow_promote_latest_model.py) to production and this model later is used for the [GUNICORN endpoint](03_deployment/gunicorn_predict_registry.py) to predict.
* Workflow orchestration
    * the workflow is orchestrated in a [MAGE pipeline](02_pipeline/mage_pipeline/dtc_persona_analysis) in a [Docker Compose](02_pipeline/mage_pipeline/docker-compose.yml) stack 
    * the stack covers `MLflow`, `MAGE`, `Postgres` and `CloudBeaver` (a database client)
* Model deployment
    * Model training is done in batch, as we are working with customer data that has no instant need for a labeling prediciton.
    * The [model deployment code](03_deployment/gunicorn_predict_registry.py) is [containerized](/Users/matthiasmotl/neuefische/repositories/dtc/dtc_persona_analysis/03_deployment/Dockerfile) and deployed on a `GUNICORN` web server that fetches the production model from the `Postgres` model registry
    * the `GUNICORN` server can be started from a [Makefile](./Makefile), target "gunicorn".
* Model monitoring
    * The comprehensive `EVIDENTLY` monitoring runs as a [MAGE conditional](/Users/matthiasmotl/neuefische/repositories/dtc/dtc_persona_analysis/02_pipeline/mage_pipeline/dtc_persona_analysis/conditionals) evaluating data drift, which is recommended in clustering problems.
    * When drift detected:
        * The conditional triggers the [MLflow experiment](02_pipeline/mage_pipeline/dtc_persona_analysis/custom/mlflow_experiment_tracking.py) to re-train a model and sends a `Telegram` notification alert.
    * When no drift detected:
        * conditional send a `Telegram` notification reporting an eventless run.
* Reproducibility
    * it's again up to you if you consider the instructions well described
    * code worked on my end in a conda environment, a [environment.yml](./environment.yml) is provided to help re-create an environment with exact dependencies.
* Best practices
    * `black` code formatter is used and can be run from the [Makefile](./Makefile)
    * A [Makefile](./Makefile) is set up to run commands for
        * `Terraform GCS` provisioning
        * `black` code formatter
        * `GUNICORN` web (server as an prediction endpoint)
        * creating the synthetic exemplarily dataset 
        * starting the `Docker` stack
    * [pre-commit hooks](./.pre-commit-config.yaml) are used  


## So, in brief overview:  

1. **End-to-End Persona Analysis Pipeline:**  
   The repository implements a full workflow for persona analysis, including data creation, model training, pipeline orchestration, deployment, monitoring, alerting.

2. **Modular Structure:**  
   The project is organized into clear stages:  
   - `00_create_data` for data generation and ingestion  
   - `01_model` for model training and experiment tracking code creation (implemented in MAGE) 
   - `02_pipeline` for pipeline orchestration (MAGE)  
   - `03_deployment` for serving models (GUNICORN) 
   - `04_monitoring` for EVIDENTLY drift and performance monitoring (implemented in MAGE)
   - `05_iac` for infrastructure-as-code (Terraform)

3. **MLflow Integration:**  
   Model training and experiment tracking are managed with MLflow, including model artifacts, experiment runs and promotions, and a Postgres database as MLflow registry.

4. **Containerization and Orchestration:**  
   The repository supports containerized workflows (Docker, Docker Compose) and pipeline orchestration (Mage), enabling reproducible and scalable ML operations.

5. **Comprehensive Documentation and Assets:**  
   Includes detailed markdown documentation, Mermaid diagrams for data flow, and visual assets to support understanding and communication of the project’s purpose and workflow.

