FROM python:3.12-slim

# Install compiler & dependencies for zeroc-ice
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libssl-dev \
    libbz2-dev \
    libexpat1-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask zeroc-ice gunicorn

WORKDIR /app