# Docker Usage Guide for XSS Validator

This document provides instructions for using Docker with the XSS Validator application.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional, for local development)

## Using Pre-built Images from GitHub Container Registry

The XSS Validator Docker image is automatically built and published to GitHub Container Registry using GitHub Actions. You can use these pre-built images instead of building the image locally.

### Pulling the Image

To pull the latest image from GitHub Container Registry:

```bash
docker pull ghcr.io/bladewing/xss-validator:latest
```

### Available Tags

The following tags are available:

- `latest`: The most recent build from the main branch
- `vX.Y.Z`: Specific version releases (e.g., `v1.0.0`)
- `vX.Y`: Major.Minor version (e.g., `v1.0`)
- `sha-XXXXXXX`: Specific commit SHA

### Running the Container from GitHub Container Registry

```bash
docker run -p 8000:8000 ghcr.io/bladewing/xss-validator:latest
```

## Building the Docker Image

To build the Docker image for the XSS Validator application, run the following command from the project root:

```bash
docker build -t xss-validator .
```

This will create a Docker image named `xss-validator` using the Dockerfile in the project root.

## Running the Container

Once the image is built, you can run the container with the following command:

```bash
docker run -p 8000:8000 xss-validator
```

This will start the XSS Validator application and expose it on port 8000 of your host machine.

You can then access the API at `http://localhost:8000`.

## Using Docker Compose for Local Development

For local development, you can use Docker Compose to simplify the process of building and running the application.

The project includes a `docker-compose.yml` file that sets up the application with volume mounts for live code reloading.

### Starting the Application

To start the application using Docker Compose, run:

```bash
docker-compose up
```

This will build the image (if needed) and start the container with the appropriate volume mounts and port mappings.

### Rebuilding the Image

If you make changes to the Dockerfile or need to rebuild the image for any reason, you can use:

```bash
docker-compose up --build
```

### Running in the Background

To run the application in the background (detached mode), use:

```bash
docker-compose up -d
```

### Stopping the Application

To stop the application, use:

```bash
docker-compose down
```

## Common Docker Commands

Here are some common Docker commands that may be useful when working with the XSS Validator application:

### View Running Containers

```bash
docker ps
```

### View Container Logs

```bash
docker logs <container_id>
```

Or with Docker Compose:

```bash
docker-compose logs
```

### Access a Shell in the Container

```bash
docker exec -it <container_id> /bin/bash
```

Or with Docker Compose:

```bash
docker-compose exec xss-validator /bin/bash
```

### Check Resource Usage

```bash
docker stats
```

## Environment Variables

The Docker container supports the following environment variables:

- `PORT`: The port on which the application will listen (default: 8000)
- `HOST`: The host address to bind to (default: 0.0.0.0)
- `PYTHONUNBUFFERED`: Set to 1 to ensure Python output is sent straight to the container log (default: 1)

Example usage:

```bash
docker run -p 9000:9000 -e PORT=9000 xss-validator
```

## Optimizations

The Dockerfile has been optimized for:

1. **Size**: Using a slim base image and cleaning up after package installation
2. **Build time**: Copying only necessary files and leveraging Docker layer caching
3. **Security**: Running as a non-root user (when possible)
4. **Performance**: Installing only production dependencies

## Troubleshooting

If you encounter issues with the Docker container, try the following:

1. Ensure Docker has enough resources allocated (memory, CPU)
2. Check the container logs for error messages
3. Verify that the required ports are not already in use
4. Make sure the container has network access to the test website

For more detailed troubleshooting, refer to the troubleshooting guide in the docs directory.
