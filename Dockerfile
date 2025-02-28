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
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into /app
COPY app/ .

# Add the current directory to Python path to ensure modules can be imported
ENV PYTHONPATH=/app

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]