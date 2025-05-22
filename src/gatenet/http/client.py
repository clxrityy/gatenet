import json
from urllib import request, parse
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError

class HTTPClient:
    """
    Lightweight HTTP client for requests using built-in urllib.
    """
    
    def __init__(self, base_url: str):
        """
        :param base_url: The base URL (e.g. http://127.0.0.1:8000)
        """
        self.base_url = base_url.rstrip("/")
        
    def get(self, path: str) -> Dict[str, Any]:
        """
        Send a GET request
        
        :param path: The route path (e.g. "/status")
        :return: Parsed JSON response
        """
        url = f"{self.base_url}{path}"
        try:
            with request.urlopen(url, timeout=5) as response:
                return json.loads(response.read())
        except HTTPError as e:
            return {
                "error": e.reason,
                "code": e.code
            }
        except URLError as e:
            return {
                "error": str(e)
            }

    def post(self, path: str, data: Dict[str, Any], headers: Optional[Dict[str, str]]) -> Dict[str, Any]:
        """
        Send a POST request with JSON body
        
        :param path: The route path (e.g. "/echo")
        :param data: Dict to send as JSON
        :return: Parsed JSON response
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {"Content-Type": "application/json"}
        
        if headers:
            final_headers.update(headers)
        
        encoded = json.dumps(data).encode()
        req = request.Request(url, data=encoded, headers=headers, method="POST")

        try:
            with request.urlopen(req, timeout=5) as response:
                return json.loads(response.read())
        except HTTPError as e:
            return {
                "error": e.reason,
                "code": e.code
            }
        except URLError as e:
            return {
                "error": str(e)
            }
