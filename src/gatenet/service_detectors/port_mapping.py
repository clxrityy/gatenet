"""
Service detection by direct port mapping.
Maps well-known ports to common service names.
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class PortMappingDetector(ServiceDetector):
    """
    Detects services by direct port mapping.
    Returns a service name for a known port, or None if not found.
    """
    PORT_MAPPING = {
        443: "HTTPS Server",
        53: "DNS Server",
        23: "Telnet Server",
        110: "POP3 Server",
        143: "IMAP Server",
        993: "IMAPS Server",
        995: "POP3S Server",
        3389: "Remote Desktop Protocol (RDP)"
    }

    def detect(self, port: int, banner: str) -> Optional[str]:
        """
        Return the mapped service name for the given port, or None if not found.

        Parameters
        ----------
        port : int
            The port number to check.
        banner : str
            The banner string (unused in this detector).

        Returns
        -------
        Optional[str]
            The detected service name, or None.
        """
        return self.PORT_MAPPING.get(port)
