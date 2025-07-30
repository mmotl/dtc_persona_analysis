# Set the Terraform directory to the current directory
TF_DIR := ./05_iac
# Set the path to the main Terraform configuration file
TF_MAIN := $(TF_DIR)/main.tf

# Target to build and run the Docker stack
PIPELINE_DIR := ./02_pipeline/mage_pipeline
COMPOSE_FILE := ${PIPELINE_DIR}/docker-compose.yml

# gunicorn directory
GUNICORN_DIR := ./03_deployment

# Target to initialize and apply Terraform configuration
tf_create:
	terraform -chdir=$(TF_DIR) init      # Initialize Terraform in the specified directory
	terraform -chdir=$(TF_DIR) apply -auto-approve  # Apply the Terraform configuration without approval prompt

# Target to destroy Terraform-managed infrastructure
tf_destroy:
	terraform -chdir=$(TF_DIR) destroy -auto-approve  # Destroy the Terraform-managed infrastructure without approval prompt

.PHONY: black

# Target to format Python scripts using black
black:
	black .
	
# Target to run the Gunicorn server
gunicorn:
	docker run -it --rm \
  --name gunicorn_webservice \
  -p 9999:9999 \
  -v "$(GUNICORN_DIR)/gcp_key.json:/app/gcp_key.json" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/app/gcp_key.json" \
  gunicorn_webservice:v1

.PHONY: docker_stack

docker_stack:
	@echo "Bringing up the Docker stack from ${COMPOSE_FILE}..."
	@docker-compose -f ${COMPOSE_FILE} up -d

# Target to create and ingest data using the create_data.py script
INGEST_TABLE=customer_features_test2
create_data:
	@echo "Creating data and ingesting into postgres database ..."
	cd 00_create_data && python create_data_wlabel.py 500 2 42 1 features_01_2025.csv
	cd 00_create_data && python ingest.py $(INGEST_TABLE) features_01_2025.csv
	cd 00_create_data && python create_data.py 500 2 42 2 features_02_2025.csv
	cd 00_create_data && python ingest.py $(INGEST_TABLE) features_02_2025.csv
	cd 00_create_data && python create_data.py 500 3.1 5977 3 features_03_2025.csv
	cd 00_create_data && python ingest.py $(INGEST_TABLE) features_03_2025.csv
	cd 00_create_data && python create_data.py 500 2 42 4 features_04_2025.csv
	cd 00_create_data && python ingest.py $(INGEST_TABLE) features_04_2025.csv

# Declare tf_create as a phony target (not a real file)
.PHONY: tf_create tf_destroy black gunicorn create_data docker_stack