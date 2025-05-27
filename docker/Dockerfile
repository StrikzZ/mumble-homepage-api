# Build-Stage: Install everything needed to build
FROM python:3.11-slim AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libssl-dev \
    libbz2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final-Stage: The real minimal image
FROM python:3.11-slim

WORKDIR /app

COPY app /app
COPY docker/docker_entrypoint.sh /app/docker_entrypoint.sh
COPY requirements.txt /app/requirements.txt

# Only take build from 
COPY --from=build /install /usr/local

RUN chmod +x /app/docker_entrypoint.sh

ENTRYPOINT ["./docker_entrypoint.sh"]