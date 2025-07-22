import json
from urllib import request
from urllib.error import HTTPError, URLError
from typing import Optional, Dict, Any


class HTTPClient:
    """
    Lightweight HTTP client for making requests using Python's built-in urllib.

    Supports GET, POST, PUT, PATCH, and DELETE methods via method chaining.
    """

    def __init__(self, base_url: str):
        """
        Initialize the HTTP client.

        Parameters
        ----------
        base_url : str
            The base URL (e.g. "http://127.0.0.1:8000").
        """
        self.base_url = base_url.rstrip("/")
        self.default_timeout = 5.0

        # Attach HTTP methods to the HTTPClient class
        # This allows us to call client.get(), client.post(), etc.
        for m in ["get", "post", "put", "patch", "delete"]:
            setattr(self, m, self._generate_method(m))
    
    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Internal method to perform an HTTP request.

        Parameters
        ----------
        method : str
            HTTP method (GET, POST, etc.).
        path : str
            Request path (relative to base_url).
        data : dict, optional
            Data to send in the request body (will be JSON-encoded).
        headers : dict, optional
            Additional headers to include in the request.
        timeout : float, optional
            Timeout for the request in seconds.

        Returns
        -------
        dict
            Parsed JSON response or error information.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {
            "Content-Type": "application/json"
        }
        
        if headers:
            final_headers.update(headers)
        
        encoded = json.dumps(data).encode() if data else None
        req = request.Request(url, data=encoded, headers=final_headers, method=method.upper())
        
        try:
            with request.urlopen(req, timeout=timeout or self.default_timeout) as response:
                resp_data = json.loads(response.read())
                return {
                    "ok": True,
                    "status": response.status,
                    "data": resp_data,
                    "error": None
                }
        except HTTPError as e:
            return {
                "error": e.reason,
                "data": None,
                "ok": False,
                "status": e.code,
            }
        except URLError as e:
            return {
                "error": str(e),
                "data": None,
                "ok": False,
                "status": None,
            }

    def _generate_method(self, method: str):
        def _method(
            path: str, 
            data: Optional[Dict] = None, 
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[float] = None
         ) -> Dict[str, Any]:
            """
            Sends an HTTP {method} request to the specified path.
            """
            return self._request(method.upper(), path, data, headers, timeout)
        
        _method.__name__ = method
        _method.__doc__ = f"Send an HTTP {method.upper()} request."
        return _method

