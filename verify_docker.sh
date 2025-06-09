#!/bin/bash
# Script to verify that the Docker container works correctly

set -e  # Exit on error

echo "=== XSS Validator Docker Verification Script ==="
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

echo "✅ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Warning: Docker Compose is not installed or not in PATH"
    echo "Some tests will be skipped"
    DOCKER_COMPOSE_AVAILABLE=false
else
    echo "✅ Docker Compose is installed"
    DOCKER_COMPOSE_AVAILABLE=true
fi

echo
echo "=== Building Docker Image ==="
docker build -t xss-validator-test .

echo
echo "=== Running Container ==="
# Run the container in detached mode
CONTAINER_ID=$(docker run -d -p 8000:8000 xss-validator-test)
echo "Container started with ID: $CONTAINER_ID"

# Wait for the container to start up
echo "Waiting for the API to become available..."
MAX_RETRIES=30
RETRY_COUNT=0
API_AVAILABLE=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8000/ > /dev/null; then
        API_AVAILABLE=true
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Waiting... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 1
done

if [ "$API_AVAILABLE" = false ]; then
    echo "Error: API did not become available within the timeout period"
    docker logs $CONTAINER_ID
    docker stop $CONTAINER_ID
    docker rm $CONTAINER_ID
    exit 1
fi

echo "✅ API is available"

echo
echo "=== Testing API Endpoints ==="

# Test root endpoint
echo "Testing root endpoint..."
ROOT_RESPONSE=$(curl -s http://localhost:8000/)
if [[ $ROOT_RESPONSE == *"XSS Validator API"* ]]; then
    echo "✅ Root endpoint working correctly"
else
    echo "❌ Root endpoint not working as expected"
    echo "Response: $ROOT_RESPONSE"
    docker logs $CONTAINER_ID
    docker stop $CONTAINER_ID
    docker rm $CONTAINER_ID
    exit 1
fi

# Test input endpoint with non-XSS payload (to avoid actual XSS execution)
echo "Testing input endpoint..."
INPUT_RESPONSE=$(curl -s "http://localhost:8000/check/input?url=http://example.com&payload=test")
if [[ $INPUT_RESPONSE == *"xss_detected"* ]]; then
    echo "✅ Input endpoint working correctly"
else
    echo "❌ Input endpoint not working as expected"
    echo "Response: $INPUT_RESPONSE"
    docker logs $CONTAINER_ID
    docker stop $CONTAINER_ID
    docker rm $CONTAINER_ID
    exit 1
fi

# Test URL endpoint with non-XSS URL (to avoid actual XSS execution)
echo "Testing URL endpoint..."
URL_RESPONSE=$(curl -s "http://localhost:8000/check/url?url=http://example.com")
if [[ $URL_RESPONSE == *"xss_detected"* ]]; then
    echo "✅ URL endpoint working correctly"
else
    echo "❌ URL endpoint not working as expected"
    echo "Response: $URL_RESPONSE"
    docker logs $CONTAINER_ID
    docker stop $CONTAINER_ID
    docker rm $CONTAINER_ID
    exit 1
fi

echo
echo "=== Checking Container Logs ==="
docker logs $CONTAINER_ID | head -n 20

echo
echo "=== Checking Container Resource Usage ==="
docker stats $CONTAINER_ID --no-stream

echo
echo "=== Cleaning Up ==="
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID

echo
echo "=== Testing with Docker Compose ==="
if [ "$DOCKER_COMPOSE_AVAILABLE" = true ]; then
    echo "Building and starting with docker-compose..."
    docker-compose up -d
    
    # Wait for the container to start up
    echo "Waiting for the API to become available..."
    RETRY_COUNT=0
    API_AVAILABLE=false
    
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if curl -s http://localhost:8000/ > /dev/null; then
            API_AVAILABLE=true
            break
        fi
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo "Waiting... ($RETRY_COUNT/$MAX_RETRIES)"
        sleep 1
    done
    
    if [ "$API_AVAILABLE" = false ]; then
        echo "Error: API did not become available within the timeout period when using docker-compose"
        docker-compose logs
        docker-compose down
        exit 1
    fi
    
    echo "✅ API is available with docker-compose"
    
    # Test root endpoint with docker-compose
    echo "Testing root endpoint with docker-compose..."
    ROOT_RESPONSE=$(curl -s http://localhost:8000/)
    if [[ $ROOT_RESPONSE == *"XSS Validator API"* ]]; then
        echo "✅ Root endpoint working correctly with docker-compose"
    else
        echo "❌ Root endpoint not working as expected with docker-compose"
        echo "Response: $ROOT_RESPONSE"
        docker-compose logs
        docker-compose down
        exit 1
    fi
    
    echo "Stopping and removing docker-compose services..."
    docker-compose down
else
    echo "Skipping Docker Compose tests as it's not available"
fi

echo
echo "=== All Tests Passed ==="
echo "The Docker container is working correctly!"
echo
echo "Note: This script only performs basic verification. For more thorough testing,"
echo "consider running the full test suite inside the container or testing with actual XSS payloads."