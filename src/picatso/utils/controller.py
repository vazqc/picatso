"""
controller.py
by Charles V
Handles backend work.
"""

import json
import logging
import pathlib

import requests

COLLECTIONS_BASE_API = "https://cataas.com/"


def make_api_call(
    base_url: str,
    endpoint="cat",
    query="?type=square&position=center&width=420&height=420&json=true",
) -> str:
    """Makes an API call and returns response text or error string."""
    url = base_url + endpoint
    if query:
        url += query
    response = None
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        status = response.status_code if response is not None else "unknown"
        return f"ERROR: HTTP {status}: {e}"
    except requests.exceptions.RequestException as e:
        return f"ERROR: Request failed: {e}"


def get_image_url_from_json(json_text: str) -> str:
    """Extract image URL from API JSON response."""
    d = json.loads(json_text)
    return d.get("url", "")


def store_data(data: str, filename: str) -> str:
    """Store data string to file in data/ folder."""
    file_path = pathlib.Path(f"data/{filename}")
    try:
        with file_path.open(mode="w") as file:
            file.write(data)
        return "Write Success"
    except OSError as error:
        logging.error("Writing to file %s failed due to: %s", file_path, error)
        return f"ERROR: File write failed: {error}"


if __name__ == "__main__":
    result = make_api_call(COLLECTIONS_BASE_API)
    if result.startswith("ERROR:"):
        print(result)
    else:
        print(get_image_url_from_json(result))
