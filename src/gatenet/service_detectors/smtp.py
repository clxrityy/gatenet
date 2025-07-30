"""
smtp.py
-------
Service detection strategy for SMTP protocol.

Public API:
    - SMTPDetector
"""
"""
Service detection strategy for SMTP protocol.
Detects SMTP servers based on port and banner string.
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class SMTPDetector(ServiceDetector):
    """
    Service detector for SMTP servers.
    Detects Postfix, Sendmail, or generic SMTP servers from port and banner.
    """
    def detect(self, port: int, banner: str) -> Optional[str]:
        """
        Detect SMTP service from port and banner string.

        Parameters
        ----------
        port : int
            The port number to check (typically 25).
        banner : str
            The banner string received from the service.

        Returns
        -------
        Optional[str]
            The detected SMTP service name, or None if not detected.
        """
        if port != 25 and 'smtp' not in banner:
            return None
        if 'postfix' in banner:
            return "Postfix SMTP"
        if 'sendmail' in banner:
            return "Sendmail SMTP"
        if 'smtp' in banner:
            return "SMTP Server"
        return None
