"""
Tests for the XSS Validator application.

This module contains tests for both the browser automation functions and the API endpoints.
"""
import asyncio

import pytest
from playwright.async_api import async_playwright
from fastapi.testclient import TestClient

from xss_validator.main import app
from xss_validator.browser import detect_popup, POPUP_TIMEOUT

# Test website URL
TEST_WEBSITE_URL = "http://hackme.ifflaender-family.de:4010/"

# XSS payload that should trigger a popup
XSS_PAYLOAD = "<Script>success()</Script>"

# URL with XSS payload
XSS_URL = "http://hackme.ifflaender-family.de:4010/search?q=%3CScript%3Esuccess%28%29%3C%2FScript%3E"

# Create a test client
client = TestClient(app)


@pytest.mark.asyncio
class TestBrowserAutomation:
    """Tests for the browser automation functions."""

    async def test_check_xss_via_input(self):
        """Test that the check_xss_via_input function correctly detects XSS."""
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navigate to the URL
            await page.goto(TEST_WEBSITE_URL)

            # Find the search input and enter the XSS payload
            await page.fill(".searchInput", XSS_PAYLOAD)

            # Submit the form (assuming the form is submitted on Enter)
            await page.press(".searchInput", "Enter")

            # Check if a popup is triggered
            result = await detect_popup(page)

            # Clean up
            await browser.close()

            assert result is True, "XSS via input field should be detected"

    async def test_check_xss_via_url(self):
        """Test that the check_xss_via_url function correctly detects XSS."""
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navigate to the URL
            await page.goto(XSS_URL)

            # Check if a popup is triggered
            result = await detect_popup(page)

            # Clean up
            await browser.close()

            assert result is True, "XSS via URL should be detected"


class TestAPI:
    """Tests for the API endpoints."""

    def test_root_endpoint(self):
        """Test that the root endpoint returns the expected response."""
        response = client.get("/")
        assert response.status_code == 200
        assert "XSS Validator API" in response.json()["message"]
        assert "/check/input" in response.json()["endpoints"]
        assert "/check/url" in response.json()["endpoints"]

    def test_check_input_endpoint(self):
        """Test that the check_input endpoint correctly detects XSS."""
        response = client.get(
            "/check/input", params={"url": TEST_WEBSITE_URL, "payload": XSS_PAYLOAD}
        )
        assert response.status_code == 200
        assert response.json()["xss_detected"] is True
        assert "XSS vulnerability detected" in response.json()["message"]

    def test_check_url_endpoint(self):
        """Test that the check_url endpoint correctly detects XSS."""
        response = client.get("/check/url", params={"url": XSS_URL})
        assert response.status_code == 200
        assert response.json()["xss_detected"] is True
        assert "XSS vulnerability detected" in response.json()["message"]

    def test_check_input_no_xss(self):
        """Test that the check_input endpoint correctly reports no XSS."""
        response = client.get(
            "/check/input", params={"url": TEST_WEBSITE_URL, "payload": "No XSS here"}
        )
        assert response.status_code == 200
        assert response.json()["xss_detected"] is False
        assert "No XSS vulnerability detected" in response.json()["message"]

    def test_check_url_no_xss(self):
        """Test that the check_url endpoint correctly reports no XSS."""
        response = client.get(
            "/check/url", params={"url": TEST_WEBSITE_URL + "search?q=No+XSS+here"}
        )
        assert response.status_code == 200
        assert response.json()["xss_detected"] is False
        assert "No XSS vulnerability detected" in response.json()["message"]

    def test_check_input_invalid_url(self):
        """Test that the check_input endpoint handles invalid URLs."""
        response = client.get(
            "/check/input", params={"url": "invalid-url", "payload": XSS_PAYLOAD}
        )
        assert response.status_code == 500
        assert "Error checking XSS" in response.json()["detail"]

    def test_check_url_invalid_url(self):
        """Test that the check_url endpoint handles invalid URLs."""
        response = client.get("/check/url", params={"url": "invalid-url"})
        assert response.status_code == 500
        assert "Error checking XSS" in response.json()["detail"]
