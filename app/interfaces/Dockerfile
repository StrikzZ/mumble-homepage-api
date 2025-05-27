FROM python:3.11-slim

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../app /app
WORKDIR /app

COPY ../docker/docker_entrypoint.sh /app/docker_entrypoint.sh

ENTRYPOINT ["./docker_entrypoint.sh"]