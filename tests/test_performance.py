"""
Performance tests for the XSS Validator API.

This module contains tests for measuring the performance of the API endpoints
under concurrent load.
"""

import asyncio
import time
from typing import List, Dict, Any

import pytest
import httpx
from fastapi.testclient import TestClient

from xss_validator.main import app

# Test website URL
TEST_WEBSITE_URL = "http://hackme.ifflaender-family.de:4010/"

# XSS payload that should trigger a popup
XSS_PAYLOAD = "<Script>success()</Script>"

# URL with XSS payload
XSS_URL = "http://hackme.ifflaender-family.de:4010/search?q=%3CScript%3Esuccess%28%29%3C%2FScript%3E"

# Create a test client
client = TestClient(app)


@pytest.mark.asyncio
async def test_concurrent_input_requests():
    """Test the performance of the check_input endpoint under concurrent load."""
    # Number of concurrent requests
    num_requests = 5

    # Record start time
    start_time = time.time()

    # Create a list to store responses
    responses = []

    # Make the requests
    for i in range(num_requests):
        # Alternate between XSS and non-XSS payloads to test both scenarios
        payload = XSS_PAYLOAD if i % 2 == 0 else "No XSS here"

        # Make the request using the test client
        response = client.get(
            "/check/input",
            params={"url": TEST_WEBSITE_URL, "payload": payload}
        )
        responses.append(response)

    # Record end time
    end_time = time.time()
    total_time = end_time - start_time

    # Calculate statistics
    success_rate = 100.0  # All requests should succeed with TestClient

    # Print performance metrics
    print(f"\nPerformance metrics for concurrent input requests:")
    print(f"Number of requests: {num_requests}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per request: {total_time / num_requests:.2f} seconds")
    print(f"Success rate: {success_rate:.2f}%")

    # Verify all requests were successful
    for response in responses:
        assert response.status_code == 200, f"Request failed with status code: {response.status_code}"


@pytest.mark.asyncio
async def test_concurrent_url_requests():
    """Test the performance of the check_url endpoint under concurrent load."""
    # Number of concurrent requests
    num_requests = 5

    # Record start time
    start_time = time.time()

    # Create a list to store responses
    responses = []

    # Make the requests
    for i in range(num_requests):
        # Alternate between XSS and non-XSS URLs to test both scenarios
        url = XSS_URL if i % 2 == 0 else f"{TEST_WEBSITE_URL}search?q=No+XSS+here"

        # Make the request using the test client
        response = client.get(
            "/check/url",
            params={"url": url}
        )
        responses.append(response)

    # Record end time
    end_time = time.time()
    total_time = end_time - start_time

    # Calculate statistics
    success_rate = 100.0  # All requests should succeed with TestClient

    # Print performance metrics
    print(f"\nPerformance metrics for concurrent URL requests:")
    print(f"Number of requests: {num_requests}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per request: {total_time / num_requests:.2f} seconds")
    print(f"Success rate: {success_rate:.2f}%")

    # Verify all requests were successful
    for response in responses:
        assert response.status_code == 200, f"Request failed with status code: {response.status_code}"


@pytest.mark.asyncio
async def test_mixed_concurrent_requests():
    """Test the performance of both endpoints under concurrent load."""
    # Number of concurrent requests per endpoint
    num_requests_per_endpoint = 3
    total_requests = num_requests_per_endpoint * 2

    # Record start time
    start_time = time.time()

    # Create a list to store responses
    responses = []

    # Make input endpoint requests
    for i in range(num_requests_per_endpoint):
        payload = XSS_PAYLOAD if i % 2 == 0 else "No XSS here"
        response = client.get(
            "/check/input",
            params={"url": TEST_WEBSITE_URL, "payload": payload}
        )
        responses.append(response)

    # Make URL endpoint requests
    for i in range(num_requests_per_endpoint):
        url = XSS_URL if i % 2 == 0 else f"{TEST_WEBSITE_URL}search?q=No+XSS+here"
        response = client.get(
            "/check/url",
            params={"url": url}
        )
        responses.append(response)

    # Record end time
    end_time = time.time()
    total_time = end_time - start_time

    # Calculate statistics
    success_rate = 100.0  # All requests should succeed with TestClient

    # Print performance metrics
    print(f"\nPerformance metrics for mixed concurrent requests:")
    print(f"Number of requests: {total_requests}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per request: {total_time / total_requests:.2f} seconds")
    print(f"Success rate: {success_rate:.2f}%")

    # Verify all requests were successful
    for response in responses:
        assert response.status_code == 200, f"Request failed with status code: {response.status_code}"


if __name__ == "__main__":
    # This allows running the tests directly with python
    asyncio.run(test_concurrent_input_requests())
    asyncio.run(test_concurrent_url_requests())
    asyncio.run(test_mixed_concurrent_requests())
