from abc import ABC, abstractmethod
from typing import Iterable

from gatenet.core.models import Device


class DiscoveryProvider(ABC):
    """Base class for all discovery mechanisms.

    A discovery provider is responsible for observing the local
    environment and returning Device objects representing discoveries.

    ```py
    class MyDiscoveryProvider(DiscoveryProvider):
        name = "My Provider"

        def discover(self) -> Iterable[Device]:
            # Implementation of discovery logic
            yield Device(ip="192.168.1.1")

    provider = MyDiscoveryProvider()
    ```
    """

    #: Human-readable name of the discovery provider.
    name: str

    #: Whether the provider is async-capable.
    async_capable: bool = False

    @abstractmethod
    def discover(self) -> Iterable[Device]:
        """Perform a discovery pass and return discovered devices.

        This method should be:
        - Passive when possible
        - Non-fatal on failures
        - Best-effort

        Returns:
            An iterable of Device objects representing discovered devices.

        ```py
        devices = provider.discover()
        for device in devices:
            print(device.ip)
        ```
        """
        raise NotImplementedError
