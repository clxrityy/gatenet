from typing import Optional
from abc import ABC, abstractmethod

class ServiceDetector(ABC):
    """
    Abstract base class for service detection strategies.
    """
    @abstractmethod
    def detect(self, port: int, banner: str) -> Optional[str]:
        pass
