# Use the official Python image as the base image
FROM python:3.13-slim

# Install system dependencies including nginx and gnupg (needed for repository key)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    python3-dev \
    portaudio19-dev \
    git \
    bash \
    nginx \
    gnupg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set noninteractive mode for apt to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Add Cloudflare WARP
RUN echo "deb http://pkg.cloudflarewarp.com/ focal main" > /etc/apt/sources.list.d/cloudflarewarp.list \
    && curl -L https://pkg.cloudflarewarp.com/cloudflare-warp.key | apt-key add - \
    && apt-get update && apt-get install -y cloudflare-warp \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# RUN Node.js build commands here
RUN git clone https://github.com/YunzheZJU/youtube-po-token-generator.git
WORKDIR /youtube-po-token-generator
RUN npm install
RUN node examples/one-shot.js
RUN node examples/one-shot.js > po_token.txt

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

# -----------------------------------------------------------
# Start script for connecting WARP VPN before launch
# -----------------------------------------------------------
COPY start.sh ./start.sh

# Ensure the script has Unix line endings and is executable
RUN sed -i 's/\r$//' ./start.sh && chmod +x ./start.sh

# Expose necessary ports
EXPOSE 8080

# Start both applications using the startup script
CMD ["/app/start.sh"]
