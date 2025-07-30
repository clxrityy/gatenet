"""
Fallback service detection using default port services.
Returns a default service name for common ports, or a generic unknown service label.
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class FallbackDetector(ServiceDetector):
    """
    Fallback detector using default port services.
    Returns a default service name for common ports, or a generic unknown service label.
    """
    DEFAULT_PORT_SERVICES = {
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S",
        3389: "RDP",
        21: "FTP",
        8080: "HTTP",
        8000: "HTTP"
    }

    def detect(self, port: int, banner: str) -> Optional[str]:
        """
        Return a default service name for the port, or a generic unknown label.

        Parameters
        ----------
        port : int
            The port number to check.
        banner : str
            The banner string (if present, returns unknown service).

        Returns
        -------
        Optional[str]
            The detected service name, or a generic unknown label.
        """
        if banner:
            return f"Unknown Service (Port {port})"
        return self.DEFAULT_PORT_SERVICES.get(port, f"Unknown Service (Port {port})")
