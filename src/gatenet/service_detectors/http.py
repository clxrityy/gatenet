"""
http.py
-------
Service detection strategy for HTTP protocol.

Public API:
    - HTTPDetector
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class HTTPDetector(ServiceDetector):
    """
    Service detector for HTTP servers.
    """
    def detect(self, port: int, banner: str) -> Optional[str]:
        if port not in [80, 8080, 8000, 443] and not banner.startswith('http'):
            return None
        if 'apache' in banner:
            return "Apache HTTP Server"
        if 'nginx' in banner:
            return "Nginx HTTP Server"
        if 'iis' in banner:
            return "Microsoft IIS"
        if banner.startswith('http'):
            return "HTTP Server"
        return None
