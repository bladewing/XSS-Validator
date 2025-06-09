# XSS Validator: Deployment Guide

This guide provides instructions for deploying the XSS Validator application in various environments.

## Prerequisites

Before deploying the XSS Validator, ensure you have the following:

- Python 3.8 or higher
- pip or uv package manager
- Git (for cloning the repository)
- Docker and Docker Compose (for containerized deployment)

## Local Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/xss-validator.git
cd xss-validator
```

### 2. Set Up a Virtual Environment

Using uv (recommended):

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Or using Python's built-in venv:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

Using uv:

```bash
uv pip install -e .
```

Or using pip:

```bash
pip install -e .
```

### 4. Install Playwright Browsers

```bash
playwright install
playwright install-deps
```

### 5. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:8000`.

## Docker Deployment

### Option 1: Using Pre-built Images from GitHub Container Registry

The XSS Validator Docker image is automatically built and published to GitHub Container Registry using GitHub Actions. This is the recommended approach for production deployments.

1. **Pull the Image**:

   ```bash
   docker pull ghcr.io/bladewing/xss-validator:main
   ```

2. **Run the Container**:

   ```bash
   docker run -p 8000:8000 ghcr.io/bladewing/xss-validator:main
   ```

   For production (detached mode):

   ```bash
   docker run -d -p 8000:8000 ghcr.io/bladewing/xss-validator:main
   ```

3. **Using with Docker Compose**:

   Create a `docker-compose.yml` file:

   ```yaml
   version: '3'
   services:
     xss-validator:
       image: ghcr.io/bladewing/xss-validator:main
       ports:
         - "8000:8000"
   ```

   Then run:

   ```bash
   docker-compose up -d
   ```

### Option 2: Building Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/xss-validator.git
cd xss-validator
```

### 2. Build and Run with Docker Compose

For development:

```bash
docker-compose up
```

For production (detached mode):

```bash
docker-compose up -d
```

### 3. Build and Run with Docker

Build the image:

```bash
docker build -t xss-validator .
```

Run the container:

```bash
docker run -p 8000:8000 xss-validator
```

The API will be available at `http://localhost:8000`.

## Cloud Deployment

### AWS Elastic Beanstalk

1. **Install the EB CLI**:

   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**:

   ```bash
   eb init -p docker xss-validator
   ```

3. **Create an Environment and Deploy**:

   ```bash
   eb create xss-validator-env
   ```

4. **Update the Application**:

   ```bash
   eb deploy
   ```

### Google Cloud Run

1. **Install the Google Cloud SDK**:

   Follow the instructions at https://cloud.google.com/sdk/docs/install

2. **Authenticate with Google Cloud**:

   ```bash
   gcloud auth login
   ```

3. **Set the Project ID**:

   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

4. **Build the Container Image**:

   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/xss-validator
   ```

5. **Deploy to Cloud Run**:

   ```bash
   gcloud run deploy xss-validator \
     --image gcr.io/YOUR_PROJECT_ID/xss-validator \
     --platform managed \
     --allow-unauthenticated \
     --memory 2Gi
   ```

### Azure Container Instances

1. **Install the Azure CLI**:

   Follow the instructions at https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

2. **Login to Azure**:

   ```bash
   az login
   ```

3. **Create a Resource Group**:

   ```bash
   az group create --name xss-validator-rg --location eastus
   ```

4. **Create a Container Registry**:

   ```bash
   az acr create --resource-group xss-validator-rg --name xssvalidatoracr --sku Basic
   ```

5. **Login to the Registry**:

   ```bash
   az acr login --name xssvalidatoracr
   ```

6. **Build and Push the Image**:

   ```bash
   docker build -t xssvalidatoracr.azurecr.io/xss-validator:main .
   docker push xssvalidatoracr.azurecr.io/xss-validator:main
   ```

7. **Deploy to Container Instances**:

   ```bash
   az container create \
     --resource-group xss-validator-rg \
     --name xss-validator \
     --image xssvalidatoracr.azurecr.io/xss-validator:main \
     --dns-name-label xss-validator \
     --ports 8000 \
     --memory 2
   ```

## Production Considerations

When deploying the XSS Validator in a production environment, consider the following:

### Security

- Use HTTPS for all communications
- Implement authentication for the API
- Restrict access to the API to authorized users only
- Run the container as a non-root user

### Performance

- Allocate sufficient resources (CPU, memory) for browser automation
- Consider implementing a queue for handling concurrent requests
- Use a load balancer for high-traffic deployments

### Monitoring

- Set up logging to a centralized log management system
- Implement monitoring and alerting for the application
- Track resource usage and performance metrics

### Scaling

- Use auto-scaling based on CPU/memory usage
- Consider using a container orchestration system like Kubernetes for larger deployments
- Implement a caching layer for frequently tested URLs

## Environment Variables

The following environment variables can be used to configure the application:

- `PORT`: The port on which the application will listen (default: 8000)
- `HOST`: The host address to bind to (default: 0.0.0.0)
- `LOG_LEVEL`: The logging level (default: info)
- `TIMEOUT`: Default timeout for browser operations in milliseconds (default: 5000)

## Deployment Checklist

Before going live with your deployment, ensure you have:

- [ ] Tested the application thoroughly
- [ ] Set up monitoring and logging
- [ ] Configured appropriate resource limits
- [ ] Implemented security measures
- [ ] Created backup and disaster recovery plans
- [ ] Documented the deployment process

## Troubleshooting

If you encounter issues during deployment, refer to the [Troubleshooting Guide](troubleshooting.md) for solutions to common problems.

For Docker-specific issues, see the [Docker Usage Guide](docker-usage.md).
