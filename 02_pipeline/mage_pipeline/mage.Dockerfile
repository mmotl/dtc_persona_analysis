# Use the official MageAI image as the base image
# OLD
FROM mageai/mageai:latest

# NEW
# FROM python:3.11-slim
# WORKDIR /app
# RUN pip install mage-ai==0.9.68

# Define a build argument for the user code path, using PROJECT_NAME environment variable
ARG USER_CODE_PATH=/home/src/${PROJECT_NAME}

# Copy the requirements.txt file into the container at the specified user code path
COPY requirements.txt ${USER_CODE_PATH}/requirements.txt

# Install Python dependencies from requirements.txt
RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt
