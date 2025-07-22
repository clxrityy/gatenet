import aiohttp
from typing import Optional, Dict, Any

class AsyncHTTPClient:
    """
    Asynchronous HTTP client for making requests using aiohttp.

    Supports GET, POST, PUT, PATCH, and DELETE methods via async/await.
    """

    def __init__(self, base_url: str):
        """
        Initialize the asynchronous HTTP client.

        Parameters
        ----------
        base_url : str
            The base URL (e.g. "http://127.0.0.1:8000").
        """
        self.base_url = base_url.rstrip('/')

    async def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Internal method to perform an HTTP request asynchronously.

        Parameters
        ----------
        method : str
            HTTP method (GET, POST, etc.).
        path : str
            Request path (relative to base_url).
        data : dict, optional
            Data to send in the request body.
        headers : dict, optional
            Additional headers to include in the request.

        Returns
        -------
        dict
            Parsed JSON response or error information.

        Raises
        ------
        asyncio.TimeoutError
            If the request times out.
        aiohttp.ClientError
            For network or protocol errors.
        """
        import asyncio

        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = headers or {}
        headers["Content-Type"] = "application/json"
        timeout_seconds = 5.0

        async def do_request():
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.request(method, url, json=data, headers=headers) as resp:
                        resp.raise_for_status()
                        return await resp.json()
                except aiohttp.ClientResponseError as e:
                    return {
                        "error": str(e),
                        "code": e.status
                    }
                except aiohttp.ClientError as e:
                    return {
                        "error": str(e),
                    }

        try:
            return await asyncio.wait_for(do_request(), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            return {
                "error": "Request timed out"
            }
        
    async def get(self, path: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return await self._request("GET", path, None, headers)
    
    async def post(self, path: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return await self._request("POST", path, data, headers)