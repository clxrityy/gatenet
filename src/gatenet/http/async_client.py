import aiohttp
from typing import Optional, Dict, Any

class AsyncHTTPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        
    async def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = 5.0,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = headers or {}
        headers["Content-Type"] = "application/json"
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
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
        
    async def get(self, path: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return await self._request("GET", path, None, headers)
    
    async def post(self, path: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return await self._request("POST", path, data, headers)