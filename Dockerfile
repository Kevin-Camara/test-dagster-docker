FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY hello.py hello.py
COPY workspace.yaml workspace.yaml

CMD ["dagit", "-h", "0.0.0.0", "-p", "3000"]
