# XSS Validator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker Build](https://github.com/bladewing/xss-validator/actions/workflows/docker-build-push.yml/badge.svg)](https://github.com/bladewing/xss-validator/actions/workflows/docker-build-push.yml)

A tool for validating Cross-Site Scripting (XSS) vulnerabilities in web applications. This application checks whether students have found a way to insert an XSS script into a website by detecting JavaScript popups triggered by the payload.

## Features

- Validates XSS payloads entered through input fields
- Validates XSS payloads passed directly via URLs
- Headless browser automation for realistic testing
- RESTful API for easy integration
- Dockerized for simple deployment
- Comprehensive test suite and documentation

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or uv package manager
- Playwright for browser automation

### Using pip/uv (Local Installation)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/xss-validator.git
   cd xss-validator
   ```

2. Create and activate a virtual environment:
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Or using Python's built-in venv
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package and dependencies:
   ```bash
   # Using uv
   uv pip install -e .

   # Or using pip
   pip install -e .
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   playwright install-deps
   ```

### Using Docker

#### Option 1: Using Pre-built Images from GitHub Container Registry

1. Pull the image from GitHub Container Registry:
   ```bash
   docker pull ghcr.io/bladewing/xss-validator:main
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 ghcr.io/bladewing/xss-validator:main
   ```

#### Option 2: Building Locally

1. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Or build and run with Docker:
   ```bash
   docker build -t xss-validator .
   docker run -p 8000:8000 xss-validator
   ```

## Usage

### Starting the API Server

```bash
python run.py
```

The API will be available at `http://localhost:8000`.

### API Endpoints

#### Check XSS via Input Field

```http
GET /check/input?url=http://example.com&payload=<script>alert(1)</script>
```

Parameters:
- `url`: The URL of the website to test
- `payload`: The XSS payload to test

#### Check XSS via URL

```http
GET /check/url?url=http://example.com/search?q=<script>alert(1)</script>
```

Parameters:
- `url`: The URL containing the XSS payload

### Example Response

```json
{
  "xss_detected": true,
  "message": "XSS vulnerability detected! The payload triggered a popup."
}
```

### Using the API with Python Requests

You can interact with the XSS Validator API using the Python requests library:

```python
import requests

# API base URL (adjust if your server is running on a different host/port)
api_base_url = "http://localhost:8000"

# Example 1: Check XSS via input field
def check_xss_via_input(url, payload):
    response = requests.get(
        f"{api_base_url}/check/input",
        params={"url": url, "payload": payload}
    )
    return response.json()

# Example 2: Check XSS via URL
def check_xss_via_url(url):
    response = requests.get(
        f"{api_base_url}/check/url",
        params={"url": url}
    )
    return response.json()

# Usage examples
if __name__ == "__main__":
    # Test website URL
    test_website = "http://example.com"

    # XSS payload
    xss_payload = "<script>alert(1)</script>"

    # URL with XSS payload
    xss_url = "http://example.com/search?q=<script>alert(1)</script>"

    # Check XSS via input field
    result1 = check_xss_via_input(test_website, xss_payload)
    print(f"Input field check result: {result1}")

    # Check XSS via URL
    result2 = check_xss_via_url(xss_url)
    print(f"URL check result: {result2}")
```

### Demo Script

You can run the included demo script to see the XSS validator in action:

```bash
python demo.py
```

## Testing

Run the test suite with pytest:

```bash
pytest
```

Run performance tests:

```bash
python check_performance.py
```

## Development

### Project Structure

```
xss-validator/
├── src/
│   └── xss_validator/
│       ├── __init__.py
│       ├── browser.py    # Browser automation
│       └── main.py       # FastAPI application
├── tests/
│   ├── test_xss_validator.py
│   └── test_performance.py
├── docs/
│   ├── deployment.md
│   ├── docker-usage.md
│   ├── limitations.md
│   └── troubleshooting.md
├── demo.py               # Demo script
├── run.py                # API server entry point
├── check_performance.py  # Performance analysis
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

### Development Guidelines

- Follow the Python development guidelines in `.junie/guidelines.md`
- Run tests after implementing new features
- Format code with Black before committing

## Documentation

For more detailed information, see the documentation in the `docs/` directory:

- [Deployment Guide](docs/deployment.md)
- [Docker Usage Guide](docs/docker-usage.md)
- [Known Limitations](docs/limitations.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Playwright](https://playwright.dev/) for browser automation
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
