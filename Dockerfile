FROM python:3.12-slim

# Install curl
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for our app and file endpoints
WORKDIR /app
RUN mkdir /status

# Copy the application script and the startup script to the container
COPY app.py startup.sh /app/

# Setup Python requirements
RUN pip install flask

# Expose 8080 for access
EXPOSE 8080

# Command wrapper
CMD ["./startup.sh"]
