"""
Service detection by banner keywords.
Detects services by searching for keywords in the banner string.
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class BannerKeywordDetector(ServiceDetector):
    """
    Detects services by banner keywords.
    Searches for known protocol keywords in the banner string.
    """
    BANNER_KEYWORDS = [
        (['telnet'], "Telnet Server"),
        (['pop3'], "POP3 Server"),
        (['imap'], "IMAP Server"),
    ]

    def detect(self, port: int, banner: str) -> Optional[str]:
        """
        Detect service by searching for protocol keywords in the banner.

        Parameters
        ----------
        port : int
            The port number (unused in this detector).
        banner : str
            The banner string to search for keywords.

        Returns
        -------
        Optional[str]
            The detected service name, or None if not found.
        """
        for keywords, name in self.BANNER_KEYWORDS:
            if any(keyword in banner for keyword in keywords):
                return name
        return None
