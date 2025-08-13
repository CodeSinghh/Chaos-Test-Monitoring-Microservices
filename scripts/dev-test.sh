#!/bin/bash

# --- Script: scripts/dev-test.sh
# --- Usage: ./scripts/dev-test.sh <version>

set -euo pipefail

# === Validate input ===
if [ $# -ne 1 ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

VERSION=$1
IMAGE_NAME="dhirajsingh6/video-service:$VERSION"
DEPLOYMENT_NAME="video-service"
APP_PATH="$(dirname "$0")/../app/video-service"

# === Step 1: Build ===
echo "> Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" "$APP_PATH"

# === Step 2: Push ===
echo "> Pushing Docker image to registry"
docker push "$IMAGE_NAME"

# === Step 3: Patch Kubernetes deployment ===
echo "> Updating K8s deployment with new image"
kubectl set image deployment/$DEPLOYMENT_NAME $DEPLOYMENT_NAME=$IMAGE_NAME

# === Step 4: Monitor rollout ===
echo "> Waiting for rollout to finish"
kubectl rollout status deployment/$DEPLOYMENT_NAME

echo "✅ Deployment updated to version $VERSION"
