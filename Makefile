# Set the Terraform directory to the current directory
TF_DIR := ./05_iac

# Set the path to the main Terraform configuration file
TF_MAIN := $(TF_DIR)/main.tf

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
	gunicorn_webservice:v1

# Declare tf_create as a phony target (not a real file)
.PHONY: tf_create tf_destroy black gunicorn