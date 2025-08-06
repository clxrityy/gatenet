from typing import Optional
from abc import ABC, abstractmethod

class ServiceDetector(ABC):
    """
    Abstract base class for service detection strategies.
    """
    @abstractmethod
    def detect(self, port: int, banner: str) -> Optional[str]:
        pass

from .banner_keyword import BannerKeywordDetector
from .coap import CoAPDetector
from .fallback import FallbackDetector
from .ftp import FTPDetector
from .generic import GenericServiceDetector
from .http import HTTPDetector
from .imap import IMAPDetector
from .mqtt import MQTTDetector
from .pop3 import POP3Detector
from .port_mapping import PortMappingDetector
from .sip import SIPDetector
from .smtp import SMTPDetector
from .ssh import SSHDetector

__all__ = [
    "ServiceDetector",
    "BannerKeywordDetector",
    "CoAPDetector",
    "FallbackDetector",
    "FTPDetector",
    "GenericServiceDetector",
    "HTTPDetector",
    "IMAPDetector",
    "MQTTDetector",
    "POP3Detector",
    "PortMappingDetector",
    "SIPDetector",
    "SMTPDetector",
    "SSHDetector",
]
