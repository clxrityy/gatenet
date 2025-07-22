import re
from typing import Optional
from abc import ABC, abstractmethod

class ServiceDetector(ABC):
    """
    Abstract base class for service detection strategies.

    All service detectors must implement the `detect` method.
    """

    @abstractmethod
    def detect(self, port: int, banner: str) -> Optional[str]:
        """
        Detect service from port and banner.

        Parameters
        ----------
        port : int
            The port number associated with the service.
        banner : str
            The banner string received from the service.

        Returns
        -------
        Optional[str]
            The detected service name/version, or None if not detected.
        """
        pass

class SSHDetector(ServiceDetector):
    """
    Service detector for SSH servers.
    """

    def detect(self, port: int, banner: str) -> Optional[str]:
        """
        Detect SSH service from port and banner.

        Parameters
        ----------
        port : int
            The port number associated with the service.
        banner : str
            The banner string received from the service.

        Returns
        -------
        Optional[str]
            The detected SSH service name/version, or None if not detected.
        """
        if port != 22 and 'ssh' not in banner:
            return None

        if 'openssh' in banner:
            version_match = re.search(r'openssh[_\s]+([\d\.]+p?\d*)', banner)
            version = version_match.group(1) if version_match else 'unknown'
            return f"OpenSSH {version}"

        if 'ssh' in banner:
            return "SSH Server"

        return None

class HTTPDetector(ServiceDetector):
    """
    Service detector for HTTP servers.
    """

    def detect(self, port: int, banner: str) -> Optional[str]:
        """
        Detect HTTP service from port and banner.

        Parameters
        ----------
        port : int
            The port number associated with the service.
        banner : str
            The banner string received from the service.

        Returns
        -------
        Optional[str]
            The detected HTTP service name/version, or None if not detected.
        """
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

class FTPDetector(ServiceDetector):
    """
    Service detector for FTP servers.
    """

    def detect(self, port: int, banner: str) -> Optional[str]:
        """
        Detect FTP service from port and banner.

        Parameters
        ----------
        port : int
            The port number associated with the service.
        banner : str
            The banner string received from the service.

        Returns
        -------
        Optional[str]
            The detected FTP service name/version, or None if not detected.
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

class SMTPDetector(ServiceDetector):
    """Detects SMTP services."""
    
    def detect(self, port: int, banner: str) -> Optional[str]:
        if port != 25 and 'smtp' not in banner:
            return None
            
        if 'postfix' in banner:
            return "Postfix SMTP"
        if 'sendmail' in banner:
            return "Sendmail SMTP"
        if 'smtp' in banner:
            return "SMTP Server"
        
        return None

class PortMappingDetector(ServiceDetector):
    """Detects services by direct port mapping."""
    
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
        return self.PORT_MAPPING.get(port)

class BannerKeywordDetector(ServiceDetector):
    """Detects services by banner keywords."""
    
    BANNER_KEYWORDS = [
        (['telnet'], "Telnet Server"),
        (['pop3'], "POP3 Server"),
        (['imap'], "IMAP Server"),
    ]
    
    def detect(self, port: int, banner: str) -> Optional[str]:
        for keywords, name in self.BANNER_KEYWORDS:
            if any(keyword in banner for keyword in keywords):
                return name
        return None

class GenericServiceDetector(ServiceDetector):
    """Detects services by generic indicators."""
    
    SERVICE_INDICATORS = {
        'mysql': 'MySQL Database',
        'postgresql': 'PostgreSQL Database', 
        'redis': 'Redis Server',
        'mongodb': 'MongoDB Database',
        'elasticsearch': 'Elasticsearch',
        'docker': 'Docker Registry',
        'jenkins': 'Jenkins CI/CD',
        'gitlab': 'GitLab',
        'apache': 'Apache Server',
        'nginx': 'Nginx Server'
    }
    
    def detect(self, port: int, banner: str) -> Optional[str]:
        for indicator, service_name in self.SERVICE_INDICATORS.items():
            if indicator in banner:
                return service_name
        return None

class FallbackDetector(ServiceDetector):
    """Fallback detector using default port services."""
    
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
        if banner:
            return f"Unknown Service (Port {port})"
        return self.DEFAULT_PORT_SERVICES.get(port, f"Unknown Service (Port {port})")

def _identify_service(port: int, banner: str) -> str:
    """
    Identify service type from port and banner.

    Parameters
    ----------
    port : int
        Port number where the service is running.
    banner : str
        Banner text received from the service.

    Returns
    -------
    str
        Identified service name and version.
    """
    banner_lower = banner.lower().strip()
    
    # Chain of responsibility pattern with service detectors
    detectors = [
        SSHDetector(),
        HTTPDetector(), 
        FTPDetector(),
        SMTPDetector(),
        PortMappingDetector(),
        BannerKeywordDetector(),
        GenericServiceDetector(),
        FallbackDetector()  # Always returns a result
    ]
    
    for detector in detectors:
        result = detector.detect(port, banner_lower)
        if result:
            return result
    
    # This should never be reached due to FallbackDetector
    return f"Unknown Service (Port {port})"