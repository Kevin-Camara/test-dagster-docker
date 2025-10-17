FROM python:3.11-slim

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Cria DAGSTER_HOME com permissão
RUN mkdir -p /app/dagster_home && \
    chown -R root:root /app/dagster_home && \
    chmod -R 755 /app/dagster_home

# Copia código
COPY hello.py workspace.yaml .

CMD ["sh","-c","dagster-webserver -h 0.0.0.0 -p 3000 & dagster-daemon run"]
