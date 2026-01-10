from gatenet.discovery.aggregate import discover_devices
from tests.conftest import duplicate_device, sample_device
from typing import List


def test_discover_devices_aggregates_results():
    devices = discover_devices()

    assert isinstance(devices, List)
    assert all(hasattr(device, "ip") for device in devices)
    assert all(hasattr(device, "hostname") for device in devices)
    assert len(devices) >= 1  # Assuming ARP discovery finds at least 1 device


def test_deduplicate_devices():
    from gatenet.discovery.aggregate import _deduplicate

    devices: List = [sample_device()]
    # Add a duplicate device
    devices.append(duplicate_device())
    deduplicated = _deduplicate(devices)

    assert len(deduplicated) == 1
    assert deduplicated[0].ip == sample_device().ip
