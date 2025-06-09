# XSS Validator: Troubleshooting Guide

This guide provides solutions for common issues you might encounter when using the XSS Validator application.

## API Issues

### API Not Responding

**Symptoms:**
- Unable to connect to the API
- Connection refused errors
- Timeout errors

**Possible Causes and Solutions:**

1. **API server is not running**
   - Start the API server using `python run.py` or `docker-compose up`
   - Check if the process is running with `ps aux | grep run.py` or `docker ps`

2. **Port conflict**
   - Check if another application is using port 8000: `lsof -i :8000`
   - Change the port in `run.py` or use the `PORT` environment variable

3. **Firewall blocking the connection**
   - Check firewall settings and allow connections to the API port
   - Try accessing the API from the same machine: `curl http://localhost:8000/`

### API Returns 500 Internal Server Error

**Symptoms:**
- API calls return 500 status code
- Error messages in the response

**Possible Causes and Solutions:**

1. **Invalid URL format**
   - Ensure the URL is properly formatted and includes the protocol (http:// or https://)
   - URL encode special characters in the payload

2. **Browser automation failure**
   - Check if Playwright is installed correctly: `playwright install`
   - Ensure the system has all required dependencies: `playwright install-deps`

3. **Memory or resource constraints**
   - Increase available memory for the application
   - Reduce the number of concurrent requests

4. **Network connectivity issues**
   - Verify that the API server can access the target website
   - Check for network restrictions or proxy requirements

## Browser Automation Issues

### XSS Not Detected When It Should Be

**Symptoms:**
- API returns `xss_detected: false` for a known XSS vulnerability
- No popup is detected during testing

**Possible Causes and Solutions:**

1. **Popup blocked by browser settings**
   - Verify that the headless browser is not configured to block popups
   - Try using a different browser engine (Firefox or WebKit instead of Chromium)

2. **Timing issues**
   - Increase the timeout value for popup detection:
     ```python
     # In browser.py
     POPUP_TIMEOUT = 10000  # 10 seconds
     ```
   - Add a delay before checking for popups to allow scripts to execute

3. **XSS payload not triggering correctly**
   - Check if the payload needs to be modified for the specific website
   - Try different variations of the XSS payload
   - Verify the payload works manually in a regular browser

4. **Website using Content Security Policy (CSP)**
   - Check the website's CSP headers: `curl -I <website_url>`
   - Modify the XSS payload to bypass CSP restrictions if possible

### Browser Crashes During Testing

**Symptoms:**
- Error messages about browser process termination
- Unexpected API failures

**Possible Causes and Solutions:**

1. **Insufficient memory**
   - Increase memory allocation for the application
   - Close other memory-intensive applications
   - If using Docker, increase container memory limits

2. **Missing browser dependencies**
   - Install required system dependencies: `playwright install-deps`
   - Check for error messages about missing libraries

3. **Browser version incompatibility**
   - Update Playwright: `pip install --upgrade playwright`
   - Reinstall browser binaries: `playwright install`

## Docker-Specific Issues

### Container Fails to Start

**Symptoms:**
- Docker container exits immediately after starting
- Error messages in Docker logs

**Possible Causes and Solutions:**

1. **Missing environment variables**
   - Check if required environment variables are set
   - Verify the `.env` file if using one

2. **Permission issues**
   - Check file permissions for mounted volumes
   - Run the container with appropriate user permissions

3. **Resource constraints**
   - Increase CPU and memory limits for the container
   - Check Docker resource allocation in Docker Desktop settings

### Browser Automation Not Working in Docker

**Symptoms:**
- Browser-related errors in container logs
- API returns errors for browser automation functions

**Possible Causes and Solutions:**

1. **Missing browser dependencies**
   - Ensure the Dockerfile includes all necessary system packages
   - Run `playwright install-deps` during container build

2. **Sandbox issues**
   - Run the browser with the `--no-sandbox` flag:
     ```python
     browser = await playwright.chromium.launch(headless=True, args=['--no-sandbox'])
     ```
   - Use the `--privileged` flag when running the container (use with caution)

3. **Display server issues**
   - Ensure the container has a virtual display server if needed
   - Add appropriate environment variables: `DISPLAY=:99`

## Performance Issues

### Slow Response Times

**Symptoms:**
- API takes a long time to respond
- Timeouts during testing

**Possible Causes and Solutions:**

1. **Too many concurrent requests**
   - Reduce the number of concurrent requests
   - Implement rate limiting or queuing

2. **Target website is slow**
   - Increase timeout values for browser operations
   - Consider caching results for repeated tests against the same URL

3. **Resource constraints**
   - Allocate more CPU and memory to the application
   - Monitor resource usage with `docker stats` or system monitoring tools

### Memory Leaks

**Symptoms:**
- Increasing memory usage over time
- Application becomes slower after extended use

**Possible Causes and Solutions:**

1. **Browser instances not being closed properly**
   - Verify that `cleanup` function is called in all code paths
   - Use `try/finally` blocks to ensure cleanup happens even on errors

2. **Accumulated browser data**
   - Restart the application periodically
   - Implement a cache clearing mechanism

## Installation Issues

### Dependency Installation Failures

**Symptoms:**
- Errors during `pip install` or `uv pip install`
- Missing dependencies when running the application

**Possible Causes and Solutions:**

1. **Python version incompatibility**
   - Verify that you're using Python 3.8+ as specified in the requirements
   - Create a new virtual environment with the correct Python version

2. **Package conflicts**
   - Install dependencies in a clean virtual environment
   - Use `uv pip install --no-deps` followed by `uv pip install` to resolve conflicts

3. **System dependencies missing**
   - Install required system packages:
     ```bash
     # Ubuntu/Debian
     apt-get update && apt-get install -y wget gnupg libglib2.0-0 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 libxcb1 libxkbcommon0 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 libatspi2.0-0
     
     # CentOS/RHEL
     yum install -y wget pango libXcomposite libXcursor libXdamage libXext libXi libXtst cups-libs libXScrnSaver libXrandr alsa-lib atk at-spi2-atk gtk3
     ```

## Getting Additional Help

If you're still experiencing issues after trying the solutions in this guide:

1. **Check the logs**
   - Application logs: Check stdout/stderr or Docker logs
   - Browser logs: Enable verbose logging in Playwright

2. **Search for similar issues**
   - Check the project's issue tracker
   - Search for similar issues with Playwright or FastAPI

3. **Gather diagnostic information**
   - Python version: `python --version`
   - Playwright version: `pip show playwright`
   - System information: OS, memory, CPU
   - Docker version (if applicable): `docker --version`

4. **Create a minimal reproducible example**
   - Isolate the issue in a small test case
   - Document the exact steps to reproduce the problem