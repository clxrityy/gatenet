"""
imap.py
-------
Service detection strategy for IMAP protocol.

Public API:
    - IMAPDetector
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class IMAPDetector(ServiceDetector):
    """
    Service detector for IMAP servers.
    Detects IMAP or IMAPS servers from port and banner.
    """
    def detect(self, port: int, banner: str) -> Optional[str]:
        if port not in (143, 993) and 'imap' not in banner.lower():
            return None
        if 'imaps' in banner.lower() or port == 993:
            return "IMAPS Server"
        if 'imap' in banner.lower():
            return "IMAP Server"
        return None
