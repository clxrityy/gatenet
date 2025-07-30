"""
pop3.py
-------
Service detection strategy for POP3 protocol.

Public API:
    - POP3Detector
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class POP3Detector(ServiceDetector):
    """
    Service detector for POP3 servers.
    Detects POP3 or POP3S servers from port and banner.
    """
    def detect(self, port: int, banner: str) -> Optional[str]:
        banner_lc = (banner or "").lower()
        if port == 995 or 'pop3s' in banner_lc:
            return "POP3S Server"
        if port == 110 or 'pop3' in banner_lc:
            return "POP3 Server"
        return None
