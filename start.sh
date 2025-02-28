#!/bin/bash
set -e

echo "Connecting Cloudflare Warp VPN..."
warp-cli connect
echo "Warp VPN connected."

# Check Cloudflare connection status
curl -s https://www.cloudflare.com/cdn-cgi/trace | grep warp= || true

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8001