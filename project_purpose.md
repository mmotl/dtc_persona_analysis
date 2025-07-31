x# DTC Persona Analysis - Project Purpose & Overview

## 🎯 Project Purpose

The **DTC Persona Analysis** repository is a complete **MLOps infrastructure** designed to solve a real-world customer segmentation and persona labeling problem for Direct-to-Consumer (DTC) businesses. This project demonstrates a production-ready machine learning pipeline that automatically classifies new customers into pre-existing marketing personas.

### Core Problem Statement

**TL;DR:** This project builds a system to automatically label new customer data with a client's existing marketing personas. The model works by predicting the closest pre-defined persona centroid, and includes monitoring to re-train and deploy a new model when the personas no longer match the incoming data.

### Real-World Context

The project is based on an actual market research scenario from the 2010s where:

1. **Client Challenge**: A company had their customer base segmented by a third-party provider into marketing personas (e.g., "Sustainable Steve", "Eco-Conscious Haley")
2. **Operational Need**: The client needed to automatically classify new survey participants into these existing persona categories
3. **Technical Solution**: Build a system that assigns new data points to the closest pre-defined cluster centroids

## 🏗️ Architecture Overview

The project implements a complete MLOps pipeline with the following key components:

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

## 🚀 Use Cases

This project serves as a **reference implementation** for:

1. **MLOps Education**: Complete pipeline demonstrating modern ML practices
2. **Customer Segmentation**: Automated persona classification systems
3. **Data Drift Monitoring**: Production-ready drift detection and response
4. **Model Deployment**: Containerized ML model serving
5. **Infrastructure Automation**: IaC for ML infrastructure

## 🎓 Learning Objectives

The project demonstrates mastery of:
- **MLOps Fundamentals**: Complete ML lifecycle management
- **Cloud Infrastructure**: GCP integration and IaC
- **Data Engineering**: Pipeline orchestration and monitoring
- **Model Deployment**: Production serving and API development
- **Best Practices**: Code quality, testing, and documentation

This repository represents a **production-grade MLOps solution** that could be directly deployed in a real business environment, making it an excellent example for learning modern machine learning operations and infrastructure. 