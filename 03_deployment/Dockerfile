FROM python:3.9-slim

WORKDIR /app

# 1. Copy only the requirements file first
COPY requirements.txt ./

# 2. Install the requirements
# This layer will be cached and only re-run if requirements.txt changes.
RUN pip install -r requirements.txt

# 3. Now copy the rest of your application code
COPY gunicorn_predict.py ./

EXPOSE 9999

# It's better to use CMD if you want to allow for easier overriding of the command
# But ENTRYPOINT is perfectly fine for this use case.
CMD [ "gunicorn", "--bind=0.0.0.0:9999", "--preload", "--timeout", "120", "--log-file", "/dev/stdout", "gunicorn_predict:app" ]