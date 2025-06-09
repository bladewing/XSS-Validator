"""
Main module for the XSS Validator API.

This module provides the FastAPI application and endpoints for validating XSS payloads.
"""

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional

from xss_validator.browser import check_xss_via_input, check_xss_via_url

app = FastAPI(
    title="XSS Validator",
    description="API for validating XSS payloads in websites",
    version="0.1.0",
)


class XSSCheckResult(BaseModel):
    """Response model for XSS check results."""

    xss_detected: bool
    message: str


@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {
        "message": "XSS Validator API",
        "description": "API for validating XSS payloads in websites",
        "endpoints": {
            "/check/input": "Check XSS via input field",
            "/check/url": "Check XSS via URL parameter",
        },
    }


@app.get("/check/input", response_model=XSSCheckResult)
async def check_input(
    url: str = Query(..., description="URL of the website to test"),
    payload: str = Query(..., description="XSS payload to test"),
):
    """
    Check if an XSS payload triggers a popup when entered into a search input.

    Args:
        url: URL of the website to test
        payload: XSS payload to test

    Returns:
        XSSCheckResult: Result of the XSS check
    """
    try:
        xss_detected = await check_xss_via_input(url, payload)

        if xss_detected:
            return XSSCheckResult(
                xss_detected=True,
                message="XSS vulnerability detected! The payload triggered a popup.",
            )
        else:
            return XSSCheckResult(
                xss_detected=False,
                message="No XSS vulnerability detected. The payload did not trigger a popup.",
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking XSS: {str(e)}")


@app.get("/check/url", response_model=XSSCheckResult)
async def check_url(
    url: str = Query(..., description="URL containing the XSS payload"),
):
    """
    Check if an XSS payload in a URL triggers a popup.

    Args:
        url: URL containing the XSS payload

    Returns:
        XSSCheckResult: Result of the XSS check
    """
    try:
        xss_detected = await check_xss_via_url(url)

        if xss_detected:
            return XSSCheckResult(
                xss_detected=True,
                message="XSS vulnerability detected! The URL triggered a popup.",
            )
        else:
            return XSSCheckResult(
                xss_detected=False,
                message="No XSS vulnerability detected. The URL did not trigger a popup.",
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking XSS: {str(e)}")
