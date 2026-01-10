from gatenet.discovery.aggregate import discover_devices


def test_discover_devices_aggregates_results():
    devices = discover_devices()

    assert isinstance(devices, list)
    assert all(hasattr(device, "ip") for device in devices)
    assert all(hasattr(device, "hostname") for device in devices)
    assert len(devices) >= 2  # Assuming ARP discovery finds at least 2 devices
    ips = [device.ip for device in devices]
    assert "192.168.1.1" in ips
    assert "192.168.1.42" in ips
