from gatenet.discovery.arp import ArpDiscovery
from typing import List


def test_parse_arp_output_basic():
    devices = ArpDiscovery().discover()
    assert isinstance(devices, List)
    assert all(hasattr(device, "ip") for device in devices)
