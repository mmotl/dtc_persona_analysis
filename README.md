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
To revert your CLI to the previously installed version, you may run:
$ gcloud components update --version 427.0.0

gunicorn --bind=0.0.0.0:9999 --preload  --timeout 120 --log-file gunicorn.log gunicorn_predict:app

docker run -it --rm \
  --name gunicorn_webservice \
  -p 9999:9999 \
  -v "$(pwd)/gcp_key.json:/app/gcp_key.json" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/app/gcp_key.json" \
  gunicorn_webservice:v1

  docker run -it --rm \
  --name gunicorn_webservice \
  -p 9999:9999 \
  gunicorn_webservice:v1

In /data is pickled baseline model


# FINAL README. 
# DTC Persona Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project is a complete MLOps pipeline for creating customer personas for a Direct-to-Consumer (DTC) business. It uses a K-Means clustering model to segment customers based on their data. The entire environment is containerized with Docker Compose and uses modern MLOps tools for orchestration, experiment tracking, and data monitoring.

## Core Features

*   **Infrastructure as Code (IaC):** Google Cloud Storage bucket is provisioned and managed using **Terraform**.
*   **Containerized Environment:** All services are orchestrated via **Docker Compose** for easy setup and consistent environments.
*   **Data Pipeline Orchestration:** **Mage** is used to manage the data transformation and model training pipeline.
*   **Experiment Tracking:** **MLflow** tracks experiments, logs models, and manages the model lifecycle.
*   **Data Drift & Monitoring:** **Evidently AI** is integrated into the pipeline to monitor for data drift, triggering model retraining when necessary.
*   **Model Serving:** A production model is served via a **Gunicorn** web service for real-time predictions.
*   **Database Management:** **PostgreSQL** serves as the backend for the MLflow Model Registry and stores customer data. **CloudBeaver** provides a web UI for easy database access.

## Architecture
## Data Flow Diagram  
![Data Flow Diagram](./images/dfd.svg)

The diagram below outlines the complete architecture of the project, from infrastructure provisioning to model serving.

## Technology Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Infrastructure** | Terraform, Google Cloud Storage (GCS) | Infrastructure as Code, Artifact Storage |
| **Containerization** | Docker, Docker Compose | Application Containerization & Orchestration |
| **Data & ML Pipeline**| Mage, MLflow, Evidently AI | Orchestration, Experiment Tracking, Data Monitoring |
| **Database** | PostgreSQL, CloudBeaver | Data Storage, Model Registry, DB Management |
| **Model Serving** | Gunicorn, Python | API for real-time predictions |
| **Code Quality** | Black | Python Code Formatting |

## Setup and Installation

### Prerequisites

*   [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
*   [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
*   [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) authenticated with your GCP account.
*   [Python](https://www.python.org/downloads/)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Configure Environment Variables

Create a `.env` file from the example template.

```bash
cp .env.example .env
```

Now, edit the `.env` file and add your specific Google Cloud project details and any other required credentials.

```env
# .env file
GCP_PROJECT_ID="your-gcp-project-id"
GCP_REGION="your-gcp-region"
GCS_BUCKET_NAME="your-unique-gcs-bucket-name"
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=dtc_persona
```

### 3. Provision Infrastructure

Use the `Makefile` to run Terraform and create the GCS bucket.

```bash
make terraform_create
```

This will initialize Terraform and apply the configuration to create the necessary cloud resources.

### 4. Launch the Application Stack

Build and run all the services using Docker Compose.

```bash
docker-compose up --build -d
```

The `-d` flag runs the containers in detached mode. You can view logs using `docker-compose logs -f`.

## Usage

Once the stack is running, you can interact with the different components:

*   **Mage Pipeline UI:** `http://localhost:6789`
    *   Trigger new pipeline runs and monitor their status.
*   **MLflow Tracking UI:** `http://localhost:5000`
    *   View experiment runs, compare parameters/metrics, and manage registered models.
*   **CloudBeaver Database UI:** `http://localhost:8978`
    *   Access the PostgreSQL database. Use the credentials from your `.env` file.

### Running a Prediction

You can use the provided script to send a request to the prediction service.

```bash
python scripts/make_prediction.py
```

Alternatively, you can use `curl` to send a direct request to the Gunicorn web service:

```bash
curl -X POST -H "Content-Type: application/json" \
--data '{"customer_id": "123", "features": [0.1, 0.5, 0.9]}' \
http://localhost:8080/predict
```

## Makefile Commands

A `Makefile` is included to simplify common tasks.

*   `make terraform_create`: Provisions the GCS infrastructure.
*   `make terraform_destroy`: Destroys the GCS infrastructure. **Use with caution.**
*   `make black`: Formats all Python code using the Black code formatter.
*   `make up`: Starts all services with `docker-compose up -d`.
*   `make down`: Stops all running services with `docker-compose down`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
