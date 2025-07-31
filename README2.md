# DTC Persona Analysis - Complete MLOps Pipeline

*MLOps infrastructure for customer persona analysis and segmentation mapping*

![Codehase](./images/bunny2.png)

## 🎯 Project Overview

The **DTC Persona Analysis** repository is a complete **MLOps infrastructure** designed to solve a real-world customer segmentation and persona labeling problem for Direct-to-Consumer (DTC) businesses. This project demonstrates a production-ready machine learning pipeline that automatically classifies new customers into pre-existing marketing personas.

### Problem Statement

**TL;DR:** This project implements a full workflow to automatically label customer data with pre-defined marketing personas. The model works by predicting the closest pre-defined persona centroid, and includes monitoring to re-train and deploy a new model when the personas no longer match the incoming data.

### Real-World Context

The project is based on an actual market research scenario from the 2010s where:

1. **Client Challenge**: A company had their customer base segmented by a third-party provider into marketing personas (e.g., "Sustainable Steve", "Eco-Conscious Haley")
2. **Operational Need**: The client needed to automatically classify new survey participants into these existing persona categories
3. **Technical Solution**: Build a system that assigns new data points to the closest pre-defined cluster centroids

### Core Objectives

- **Primary**: Develop a robust and automated classification model that assigns new survey participants to the most appropriate marketing persona based on proximity to provided persona centroids
- **Secondary**: Implement a data monitoring system that tracks statistical distribution changes and triggers model re-training when data drift is detected

## 🏗️ Architecture Overview

### Data Flow Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Creation │───▶│  Model Training  │───▶│ Model Deployment│
│   & Ingestion   │    │  & Experiment    │    │  & Serving      │
└─────────────────┘    │   Tracking       │    └─────────────────┘
                       └──────────────────┘              │
                                │                        │
                       ┌──────────────────┐              │
                       │   Data Pipeline  │              │
                       │   Orchestration  │              │
                       └──────────────────┘              │
                                │                        │
                       ┌──────────────────┐              │
                       │   Monitoring &   │◀─────────────┘
                       │   Drift Detection│
                       └──────────────────┘
```

### Architecture: Data Flow Diagram
![Data Flow Diagram](./images/dfd.svg)

The diagram outlines the complete architecture of the project, from infrastructure provisioning to model serving. The diagram can be adapted easily via the mermaid code in `dfd.mermaid`.

## 📁 Repository Structure

### `00_create_data/` - Data Generation & Ingestion
- **Purpose**: Creates synthetic customer data that mimics real-world persona clustering
- **Key Files**:
  - `create_data.py` - Generates artificial customer data with known persona centroids
  - `ingest.py` - Loads data into PostgreSQL database
  - `create_data.ipynb` - Interactive data creation and exploration

### `01_model/` - Model Development & Experiment Tracking
- **Purpose**: K-Means clustering model development with MLflow experiment tracking
- **Key Features**:
  - Experiment tracking with MLflow
  - Model registry management
  - Silhouette score optimization for optimal cluster count
  - Pre-trained model artifacts

### `02_pipeline/` - Data Pipeline Orchestration
- **Purpose**: Mage-based pipeline for automated data processing and model training
- **Key Components**:
  - Data transformation workflows
  - Model training automation
  - Integration with MLflow and Evidently AI
  - Docker Compose orchestration

### `03_deployment/` - Model Serving & API
- **Purpose**: Production model deployment with REST API endpoints
- **Key Features**:
  - Gunicorn web service for real-time predictions
  - Docker containerization
  - Model loading from registry or GCS
  - API testing scripts

### `04_monitoring/` - Data Drift Detection
- **Purpose**: Continuous monitoring of data distribution changes
- **Key Features**:
  - Evidently AI integration for drift detection
  - Statistical distribution monitoring
  - Automated retraining triggers

### `05_iac/` - Infrastructure as Code
- **Purpose**: Terraform-based cloud infrastructure provisioning
- **Key Components**:
  - Google Cloud Storage bucket creation
  - Infrastructure automation
  - Cloud resource management

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Infrastructure** | Terraform, Google Cloud Storage | IaC, Artifact Storage |
| **Containerization** | Docker, Docker Compose | Application Containerization |
| **Data Pipeline** | Mage, MLflow, Evidently AI | Orchestration, Experiment Tracking, Monitoring |
| **Database** | PostgreSQL, CloudBeaver | Data Storage, Model Registry, DB Management |
| **Model Serving** | Gunicorn, Python | API for Real-time Predictions |
| **Code Quality** | Black, Pre-commit hooks | Code Formatting, Security Checks |
| **Development** | Makefile | Task Automation |

## 🔄 MLOps Workflow

### 1. Data Pipeline
- **Reference Data**: January customer data serves as baseline
- **Current Data**: Monthly customer data for drift detection
- **Drift Detection**: March data triggers model retraining due to significant distribution changes

### 2. Model Lifecycle
- **Training**: K-Means clustering with optimal silhouette scores
- **Registration**: Best models stored in MLflow registry
- **Promotion**: Top-performing models promoted to production
- **Serving**: Real-time predictions via REST API

### 3. Monitoring & Retraining
- **Continuous Monitoring**: Evidently AI tracks data distribution changes
- **Automated Triggers**: Drift detection initiates model retraining
- **Quality Assurance**: Model performance validation before deployment

## 🚀 Setup and Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) authenticated with your GCP account
- [Python](https://www.python.org/downloads/)

### 1. Clone the Repository

```bash
git clone git@github.com:mmotl/dtc_persona_analysis.git
cd dtc_persona_analysis
```

### 2. Configure Environment

Create a `.env` file from the example template:

```bash
cp .env.example .env
```

Edit the `.env` file with your specific Google Cloud project details:

```env
GCP_PROJECT_ID="your-gcp-project-id"
GCP_REGION="your-gcp-region"
GCS_BUCKET_NAME="your-unique-gcs-bucket-name"
POSTGRES_USER="align_with_docker-compose"
POSTGRES_PASSWORD="align_with_docker-compose"
POSTGRES_DB="align_with_docker-compose"
```

Duplicate the .env to the Mage pipeline folder:
```bash
cp .env 02_pipeline/mage_pipeline/.env
```

Create a conda environment:
```bash
conda env create -f environment.yml -n <your_new_env_name>
```

Create a data subfolder:
```bash
mkdir data
```

### 3. Provision Infrastructure

Use the Makefile to run Terraform and create the GCS bucket:

```bash
make tf_create
```

*Note: You can use the `docker-compose_local.yml` for local-only artifact storage without cloud resources.*

### 4. Launch the Application Stack

Build and run all services using Docker Compose:

```bash
cd 02_pipeline/mage_pipeline
docker-compose up --build -d
```

The `-d` flag runs the containers in detached mode. View logs using `docker-compose logs -f`.

## 📊 Usage

Once the stack is running, you can interact with the different components:

### Web Interfaces

- **Mage Pipeline UI:** `http://localhost:6789`
  - Trigger new pipeline runs and monitor their status
- **MLflow Tracking UI:** `http://localhost:5050`
  - View experiment runs, compare parameters/metrics, and manage registered models
- **CloudBeaver Database UI:** `http://localhost:8978`
  - Access the PostgreSQL database using credentials from your `.env` file
  - *Note: First-time setup requires admin credentials for the UI only*

### Data Ingestion

Ingest artificial data into the database:

```bash
make create_data
```

This creates data for January to April 2025, with 500 customer observations each month. March data contains significant drift to trigger model retraining.

### Pipeline Execution

1. **Load Reference Data**: In Mage, load January data as "reference" data
2. **Load Current Data**: Load March data as "current" data to trigger drift detection
3. **Model Training**: Choose dataset (reference or current) for model training
4. **Drift Detection**: Evidently AI detects drift in March data and triggers retraining

### Model Serving

Start the Gunicorn web service:

```bash
make gunicorn
```

### Running Predictions

Test the prediction service:

```bash
cd 03_deployment
python test_gunicorn.py
```

## 🎯 Key Features

### ✅ Complete MLOps Implementation
- **Experiment Tracking**: MLflow for model versioning and comparison
- **Model Registry**: Centralized model management and deployment
- **Data Pipeline**: Automated data processing and model training
- **Model Deployment**: Containerized production serving
- **Monitoring**: Real-time drift detection and alerting
- **Infrastructure**: IaC with Terraform for cloud resources

### ✅ Production-Ready Components
- **Containerization**: Docker-based deployment
- **API Service**: RESTful prediction endpoints
- **Database Integration**: PostgreSQL for data persistence
- **Cloud Storage**: GCS for model artifacts
- **Monitoring**: Automated drift detection and retraining

### ✅ Development Best Practices
- **Code Quality**: Black formatting, pre-commit hooks
- **Documentation**: Comprehensive README and architecture diagrams
- **Reproducibility**: Conda environment, dependency management
- **Testing**: API testing scripts and validation

## 🎓 Learning Objectives

This project demonstrates mastery of:
- **MLOps Fundamentals**: Complete ML lifecycle management
- **Cloud Infrastructure**: GCP integration and IaC
- **Data Engineering**: Pipeline orchestration and monitoring
- **Model Deployment**: Production serving and API development
- **Best Practices**: Code quality, testing, and documentation

## 🚀 Use Cases

This project serves as a **reference implementation** for:

1. **MLOps Education**: Complete pipeline demonstrating modern ML practices
2. **Customer Segmentation**: Automated persona classification systems
3. **Data Drift Monitoring**: Production-ready drift detection and response
4. **Model Deployment**: Containerized ML model serving
5. **Infrastructure Automation**: IaC for ML infrastructure

## 📋 Evaluation Guidelines

For the MLOps Zoomcamp evaluation, refer to the [evaluation.md](./evaluation.md) file for detailed assessment criteria and scoring guidelines.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

This repository represents a **production-grade MLOps solution** that could be directly deployed in a real business environment, making it an excellent example for learning modern machine learning operations and infrastructure. 