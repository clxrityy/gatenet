"""
Service detection by generic indicators.
Detects services by searching for known software indicators in the banner string.
"""
from typing import Optional
from .ssh import ServiceDetector

from gatenet.service_detectors import ServiceDetector

class GenericServiceDetector(ServiceDetector):
    """
    Detects services by generic indicators.
    Searches for known software names in the banner string.
    """
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
        """
        Detect service by searching for known software indicators in the banner.

        Parameters
        ----------
        port : int
            The port number (unused in this detector).
        banner : str
            The banner string to search for indicators.

        Returns
        -------
        Optional[str]
            The detected service name, or None if not found.
        """
        for indicator, service_name in self.SERVICE_INDICATORS.items():
            if indicator in banner:
                return service_name
        return None
