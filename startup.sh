#!/bin/bash

# Pipe Holders
STARTUP_PIPE=/startup
READY_PIPE=/ready
HEALTHZ_PIPE=/healthz

# Create named pipes
mkfifo $STARTUP_PIPE 2>/dev/null
mkfifo $READY_PIPE 2>/dev/null
mkfifo $HEALTHZ_PIPE 2>/dev/null

# Default to Port 8080 if env not set
PORT=${PORT:-8080}

# Independent pipe watchers
while true; do
    if [ -p "$STARTUP_PIPE" ]; then
        curl -s http://localhost:$PORT/startup > "$STARTUP_PIPE"
    fi
done &

while true; do
    if [ -p "$READY_PIPE" ]; then
        curl -s http://localhost:$PORT/ready > "$READY_PIPE"
    fi
done &

while true; do
    if [ -p "$HEALTHZ_PIPE" ]; then
        curl -s http://localhost:$PORT/healthz > "$HEALTHZ_PIPE"
    fi
done &

# Start Python application
echo "Starting Python Flask application"
python app.py
