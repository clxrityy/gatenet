from gatenet.discovery.arp import discover_arp
from typing import List


def test_parse_arp_output_basic():
    devices = discover_arp()
    assert isinstance(devices, List)
    assert all(hasattr(device, "ip") for device in devices)
