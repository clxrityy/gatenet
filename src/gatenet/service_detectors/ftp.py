"""
Service detection strategy for FTP protocol.
Detects FTP servers based on port and banner string.
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class FTPDetector(ServiceDetector):
    """
    Service detector for FTP servers.
    Detects vsftpd, FileZilla, or generic FTP servers from port and banner.
    """
    def detect(self, port: int, banner: str) -> Optional[str]:
        """
        Detect FTP service from port and banner string.

        Parameters
        ----------
        port : int
            The port number to check (typically 21).
        banner : str
            The banner string received from the service.

        Returns
        -------
        Optional[str]
            The detected FTP service name, or None if not detected.
        """
        if port != 21 and 'ftp' not in banner:
            return None
        if 'vsftpd' in banner:
            return "vsftpd FTP Server"
        if 'filezilla' in banner:
            return "FileZilla FTP Server"
        if 'ftp' in banner:
            return "FTP Server"
        return None
