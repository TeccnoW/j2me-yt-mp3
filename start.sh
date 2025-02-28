#!/bin/bash
set -e

echo "Connecting Cloudflare Warp VPN..."
warp-cli connect
echo "Warp VPN connected."

# Check Cloudflare connection status
if curl -s https://www.cloudflare.com/cdn-cgi/trace | grep -q 'warp=on'; then
  echo "Warp is ON."
else
  echo "Warp is OFF. Exiting."
  exit 1
fi

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8001