import os
import requests
from urllib.parse import urlparse


class CurlCommand :
    def __init__(self):
        self.name = "curl"
        self.flags = ["url"]
        self.description = "Retrieve the content of a webpage"

    def run(self, *args):
        if len(args) != 1:
            return "curl: exactly one URL is required"
        url = args[0]
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            # Determine a safe filename
            parsed = urlparse(url)
            name = os.path.basename(parsed.path) or "index.html"
            # Avoid overwriting existing files by appending a numeric suffix
            base, ext = os.path.splitext(name)
            candidate = name
            i = 1
            while os.path.exists(candidate):
                candidate = f"{base}_{i}{ext}"
                i += 1
            with open(candidate, 'wb') as f:
                f.write(response.content)
            return f"Saved: {candidate} ({len(response.content)} bytes)"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
