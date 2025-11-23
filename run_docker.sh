#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t brazil-retail-backend .

# Run the Docker container
# We mount the .env file to pass environment variables
echo "Running Docker container..."
docker run -d \
  --name brazil-retail-api \
  -p 8000:8000 \
  --env-file .env \
  brazil-retail-backend

echo "Container started. API available at http://localhost:8000"
echo "Health check: http://localhost:8000/health"
