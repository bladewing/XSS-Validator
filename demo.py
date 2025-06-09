"""
Demo script for the XSS Validator application.

This script demonstrates the functionality of the XSS validator by checking
for XSS vulnerabilities in the specified URLs.
"""

import asyncio
from xss_validator.browser import check_xss_via_input, check_xss_via_url

# Test website URL
TEST_WEBSITE_URL = "http://hackme.ifflaender-family.de:4010/"

# XSS payload that should trigger a popup
XSS_PAYLOAD = "<Script>success()</Script>"

# URL with XSS payload
# Try different URL encodings
XSS_URL = "http://hackme.ifflaender-family.de:4010/search?q=<Script>success()</Script>"
XSS_URL_ENCODED = "http://hackme.ifflaender-family.de:4010/search?q=%3CScript%3Esuccess%28%29%3C%2FScript%3E"


async def main():
    """Run the demo."""
    print("XSS Validator Demo")
    print("=================")

    # Check XSS via input field
    print("\nChecking XSS via input field...")
    print(f"URL: {TEST_WEBSITE_URL}")
    print(f"Payload: {XSS_PAYLOAD}")

    try:
        result = await check_xss_via_input(TEST_WEBSITE_URL, XSS_PAYLOAD)
        if result:
            print("✅ XSS vulnerability detected! The payload triggered a popup.")
        else:
            print(
                "❌ No XSS vulnerability detected. The payload did not trigger a popup."
            )
    except Exception as e:
        print(f"❌ Error checking XSS via input field: {e}")

    # Check XSS via URL (non-encoded)
    print("\nChecking XSS via URL (non-encoded)...")
    print(f"URL: {XSS_URL}")

    try:
        result = await check_xss_via_url(XSS_URL)
        if result:
            print("✅ XSS vulnerability detected! The URL triggered a popup.")
        else:
            print("❌ No XSS vulnerability detected. The URL did not trigger a popup.")
    except Exception as e:
        print(f"❌ Error checking XSS via URL: {e}")

    # Check XSS via URL (encoded)
    print("\nChecking XSS via URL (encoded)...")
    print(f"URL: {XSS_URL_ENCODED}")

    try:
        result = await check_xss_via_url(XSS_URL_ENCODED)
        if result:
            print("✅ XSS vulnerability detected! The URL triggered a popup.")
        else:
            print("❌ No XSS vulnerability detected. The URL did not trigger a popup.")
    except Exception as e:
        print(f"❌ Error checking XSS via URL: {e}")


if __name__ == "__main__":
    asyncio.run(main())
