# Use the official Python image as the base image
FROM python:3.13-slim

# Install system dependencies including nginx
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    python3-dev \
    portaudio19-dev \
    git \
    bash \
    nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# RUN Node.js build commands here
RUN git clone https://github.com/YunzheZJU/youtube-po-token-generator.git
WORKDIR /youtube-po-token-generator
RUN npm install
RUN node /content/youtube-po-token-generator/examples/one-shot.js
RUN node /content/youtube-po-token-generator/examples/one-shot.js > po_token.txt

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