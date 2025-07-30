"""
sip.py
------
Service detection strategy for SIP protocol.

Public API:
    - SIPDetector
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class SIPDetector(ServiceDetector):
    """
    Service detector for SIP servers.
    Detects SIP servers from port and banner.
    """
    def detect(self, port: int, banner: str) -> Optional[str]:
        if port != 5060 and 'sip' not in banner.lower():
            return None
        if 'sip' in banner.lower():
            return "SIP Server"
        return None
