#!/bin/bash


set -a
echo "Checking for .env file"
if [ -f .env ]; then
    echo "Loading custom environmental variables"
    if source .env; then
        echo "Loaded custom environmental variables"
    else
        echo "Failed to load .env file – invalid syntax?" >&2
        exit 1
    fi
else
    echo "Custom environmental file not found, using standard configuration"
fi
set +a
echo "Starting API"

gunicorn -w 1 -b 0.0.0.0:${API_PORT:-6504} ./app/api:app