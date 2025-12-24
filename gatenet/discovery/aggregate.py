# gatenet/discovery/aggregate.py

from typing import List

from gatenet.core.models import Device, Service, Port


def discover_devices() -> List[Device]:
    """
    Discover devices on the local network.

    NOTE:
    This is a stub implementation used to validate
    CLI, packaging, and output formatting.
    """

    return [
        Device(
            ip="192.168.1.1",
            hostname="router.local",
            services=[
                Service(
                    name="http",
                    ports=[Port(number=80)]
                )
            ]
        ),
        Device(
            ip="192.168.1.42",
            hostname="laptop.local",
            services=[]
        )
    ]
