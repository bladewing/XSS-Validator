import requests

# API base URL (adjust if your server is running on a different host/port)
api_base_url = "https://xss.ifflaender-family.de/"


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
    test_website = "http://hackme.ifflaender-family.de:4010/"

    # XSS payload
    xss_payload = "<script>success()</script>"
    # Check XSS via input field
    result1 = check_xss_via_input(test_website, xss_payload)
    print(f"Input field check result: {result1}")

    if result1["xss_detected"]:
        print("Grade:=>> 100")
