"""
ssh.py
-------
Service detection strategy for SSH protocol.

This module provides the SSHDetector and ServiceDetector ABC for extensible service detection.

Public API:
    - ServiceDetector
    - SSHDetector
"""

from typing import Optional
import re
from gatenet.service_detectors import ServiceDetector

class SSHDetector(ServiceDetector):
    """
    Service detector for SSH servers.
    """
    def detect(self, port: int, banner: str) -> Optional[str]:
        if port != 22 and 'ssh' not in banner:
            return None
        if 'openssh' in banner:
            version_match = re.search(r'openssh[_\s]+([\d\.]+p?\d*)', banner)
            version = version_match.group(1) if version_match else 'unknown'
            return f"OpenSSH {version}"
        if 'ssh' in banner:
            return "SSH Server"
        return None
