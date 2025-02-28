# Use the official Python image as the base image
FROM python:3.13-slim

# Install system dependencies including nginx, git, bash, and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    python3-dev \
    portaudio19-dev \
    git \
    bash \
    nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------
# Install Cloudflare Warp CLI for free VPN
RUN curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | apt-key add - && \
    echo "deb https://pkg.cloudflareclient.com/ buster main" > /etc/apt/sources.list.d/cloudflare-client.list && \
    apt-get update && apt-get install -y cloudflare-warp && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------
# Install Node.js
# -----------------------------------------------------------
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------
# Build steps for the Node.js project
# -----------------------------------------------------------
RUN git clone https://github.com/YunzheZJU/youtube-po-token-generator.git
WORKDIR /youtube-po-token-generator
RUN npm install
RUN node examples/one-shot.js
RUN node examples/one-shot.js > po_token.txt

# -----------------------------------------------------------
# Set up FastAPI Application
# -----------------------------------------------------------
WORKDIR /app

# Copy and install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code
COPY app/ .

# Ensure Python can find your modules
ENV PYTHONPATH=/app

# -----------------------------------------------------------
# Add entrypoint script for connecting Warp VPN before launch
# -----------------------------------------------------------
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8001

# Use the entrypoint script as the container’s entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Note:
# To allow the Warp VPN to modify network settings, you might need to run the container with:
#   --cap-add=NET_ADMIN --device /dev/net/tun
