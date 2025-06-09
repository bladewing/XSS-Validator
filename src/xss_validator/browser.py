"""
Browser automation module for XSS validation.

This module provides functions for initializing a browser in headless mode,
detecting popups, and cleaning up browser instances.
"""

import asyncio
from typing import Optional, Tuple, Dict, Any

from playwright.async_api import async_playwright, Browser, Page, Playwright

# Timeout for popup detection in milliseconds
POPUP_TIMEOUT = 5000  # 5 seconds


async def initialize_browser() -> Tuple[Playwright, Browser, Page]:
    """
    Initialize a browser in headless mode.

    Returns:
        Tuple containing the playwright instance, browser instance, and page instance.
    """
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()

    return playwright, browser, page


async def detect_popup(page: Page, timeout: int = POPUP_TIMEOUT) -> bool:
    """
    Detect if a popup (alert, confirm, prompt) is triggered.

    Args:
        page: The page instance to monitor.
        timeout: Timeout in milliseconds (default: 5000ms).

    Returns:
        True if a popup was detected, False otherwise.
    """
    popup_detected = False

    async def handle_dialog(dialog):
        nonlocal popup_detected
        popup_detected = True
        await dialog.accept()

    page.on("dialog", handle_dialog)

    # Wait for the specified timeout
    try:
        await asyncio.sleep(timeout / 1000)  # Convert ms to seconds
    except asyncio.CancelledError:
        pass

    return popup_detected


async def cleanup(playwright: Playwright, browser: Browser) -> None:
    """
    Clean up browser and playwright instances.

    Args:
        playwright: The playwright instance to close.
        browser: The browser instance to close.
    """
    await browser.close()
    await playwright.stop()


async def check_xss_via_input(url: str, xss_payload: str) -> bool:
    """
    Check if an XSS payload triggers a popup when entered into a search input.

    Args:
        url: The URL of the website to test.
        xss_payload: The XSS payload to test.

    Returns:
        True if a popup was detected, False otherwise.
    """
    playwright, browser, page = await initialize_browser()

    try:
        # Navigate to the URL
        await page.goto(url)

        # Find the search input and enter the XSS payload
        await page.fill(".searchInput", xss_payload)

        # Submit the form (assuming the form is submitted on Enter)
        await page.press(".searchInput", "Enter")

        # Check if a popup is triggered
        return await detect_popup(page)
    finally:
        # Clean up
        await cleanup(playwright, browser)


async def check_xss_via_url(url: str, timeout: int = POPUP_TIMEOUT * 2) -> bool:
    playwright, browser, page = await initialize_browser()

    try:
        # Registriere den Dialog-Handler VOR der Navigation
        popup_detected = False

        async def handle_dialog(dialog):
            nonlocal popup_detected
            popup_detected = True
            await dialog.accept()

        page.on("dialog", handle_dialog)

        # Navigiere zur URL
        await page.goto(url)

        # Warte die angegebene Zeit
        await asyncio.sleep(timeout / 1000)  # Konvertiere ms in Sekunden

        return popup_detected
    finally:
        # Bereinigen
        await cleanup(playwright, browser)