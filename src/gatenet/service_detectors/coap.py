"""
coap.py
-------
Service detection strategy for CoAP protocol.

Public API:
    - CoAPDetector
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class CoAPDetector(ServiceDetector):
    """
    Service detector for CoAP servers.
    Detects CoAP servers from port and banner.
    """
    def detect(self, port: int, banner: str) -> Optional[str]:
        if port != 5683 and 'coap' not in banner.lower():
            return None
        if 'coap' in banner.lower():
            return "CoAP Server"
        return None
