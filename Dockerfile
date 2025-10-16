FROM python:3.12-slim

RUN pip install dagster dagster-docker

COPY . /app
WORKDIR /app

CMD ["dagster", "api", "grpc", "--python-file", "your_pipeline_file.py", "--host", "0.0.0.0"]
