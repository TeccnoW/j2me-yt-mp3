# Use the official Python image as the base image
FROM python:3.13-slim

# Install system dependencies including nginx
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    python3-dev \
    portaudio19-dev \
    bash \
    nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# --------------------
# FastAPI Application Setup
# --------------------

# Copy requirements and install dependencies
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into /app/app
COPY app/ ./app/

# --------------------
# NGINX Configuration
# --------------------

# Copy NGINX configuration
COPY nginx.conf /etc/nginx/nginx.conf

# --------------------
# Startup Script
# --------------------

# Copy the startup script to /app and fix its line endings and permissions
COPY start.sh ./start.sh
RUN sed -i 's/\r$//' ./start.sh && chmod +x ./start.sh

# Expose NGINX port
EXPOSE 8080

# Start the application using the startup script
CMD ["/app/start.sh"]