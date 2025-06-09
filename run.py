"""
Entry point script for the XSS Validator application.

This script runs the FastAPI application using uvicorn.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("xss_validator.main:app", host="0.0.0.0", port=8000, reload=True)
