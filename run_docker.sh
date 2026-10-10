#!/usr/bin/env bash
set -euo pipefail

IMAGE=brazil-retail-backend
CONTAINER=brazil-retail-api

echo "Building ${IMAGE}..."
docker build -t "${IMAGE}" .

echo "Starting ${CONTAINER} on :8000..."
docker rm -f "${CONTAINER}" 2>/dev/null || true
docker run -d \
  --name "${CONTAINER}" \
  -p 8000:8000 \
  --env-file .env \
  "${IMAGE}"

echo "API:  http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "Health check: http://localhost:8000/health"
