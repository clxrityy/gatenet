from abc import ABC, abstractmethod
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class BackendResult:
    ok: bool
    message: str = ""

class HotspotBackend(ABC):
    @abstractmethod
    def start(self) -> BackendResult: ...

    @abstractmethod
    def stop(self) -> BackendResult: ...

    @abstractmethod
    def devices(self) -> List[Dict[str, str]]: ...
