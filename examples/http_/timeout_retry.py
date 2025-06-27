import time


def retry_request(client, path, retries=3, delay=1):
    """
    Retry a request to the specified path with a delay between attempts.
    """
    for attempt in range(retries):
        try:
            return client.get(path, timeout=1)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    return {
        "error": "All retries failed"
    }