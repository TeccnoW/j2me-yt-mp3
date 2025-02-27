#!/bin/bash
set -e

# Function to wait for a service to be ready
wait_for_service() {
    local url=$1
    echo "Waiting for $url to be ready..."
    until curl -sf "$url" > /dev/null; do
        sleep 1
        echo "Still waiting for $url..."
    done
    echo "$url is ready!"
}

# Start FastAPI Application on port 8001
echo "Starting FastAPI on port 8001..."
cd /app/app
uvicorn main:app --host 127.0.0.1 --port 8001 &
APP1_PID=$!

# Wait for FastAPI to be ready
wait_for_service "http://127.0.0.1:8001"

# Start NGINX on port 8080
echo "Starting NGINX on port 8080..."
nginx -g "daemon off;" &
NGINX_PID=$!

# Function to handle termination signals
shutdown() {
    echo "Shutting down..."
    kill $APP1_PID $NGINX_PID
    exit 0
}

# Trap termination signals and call shutdown
trap shutdown SIGINT SIGTERM

# Wait for all background processes to finish
wait