# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY pyproject.toml ./
COPY src/ ./src/
COPY run.py ./

# Install the project and its dependencies
RUN pip install --no-cache-dir -e .

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "run.py"]