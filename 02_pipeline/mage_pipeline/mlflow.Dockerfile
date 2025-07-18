# Start from the official MLflow image
FROM ghcr.io/mlflow/mlflow:v2.22.0

# Python clients for PostgreSQL and Google Cloud Storage
RUN pip install psycopg2-binary google-cloud-storage

# for debugging purposes, copy the gcp_test.py script into the container
ARG USER_CODE_PATH=/home/src/${PROJECT_NAME}
COPY gcp_test.py ${USER_CODE_PATH}/gcp_test.py 

# --- Add these lines for debugging ---
# Downloads and installs the gcloud CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update && apt-get install -y google-cloud-sdk
# ------------------------------------