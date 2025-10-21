#!/bin/bash
# Script di build locale per test
set -e

echo "========================================="
echo "Build Addon Llama.cpp Home Assistant"
echo "========================================="
echo ""

# Parametri
ARCH="${1:-amd64}"
VERSION="1.0.0"
IMAGE_NAME="local/llamacpp-addon:${VERSION}-${ARCH}"

echo "Architettura: ${ARCH}"
echo "Versione: ${VERSION}"
echo "Immagine: ${IMAGE_NAME}"
echo ""

# Build
echo "Avvio build Docker..."
docker build \
    --build-arg BUILD_FROM="ghcr.io/home-assistant/${ARCH}-base:latest" \
    -t "${IMAGE_NAME}" \
    -f Dockerfile \
    .

echo ""
echo "✓ Build completata con successo!"
echo ""
echo "Per eseguire l'addon localmente:"
echo "  docker run -p 8080:8080 -p 5000:5000 \\"
echo "    -e MODEL_URL='https://huggingface.co/...' \\"
echo "    ${IMAGE_NAME}"
echo ""
