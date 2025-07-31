# Makefile for running local MLflow server

.PHONY: server
mlflowserver:
	@echo "Starting MLflow server from Makefile"
	mlflow server \
	    --backend-store-uri sqlite:///mlflow.db \
	    --default-artifact-root ./artifacts \
	    --host 0.0.0.0 \
	    --port 5001