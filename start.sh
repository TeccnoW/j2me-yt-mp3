#!/bin/bash
set -e

echo "Connecting Cloudflare Warp VPN..."
# Connect to the free Warp VPN
warp-cli connect
echo "Warp VPN connected."

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8001
