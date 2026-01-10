from gatenet.discovery.arp import discover_arp


def test_parse_arp_output_basic():
    devices = discover_arp()

    assert len(devices) == 2
    assert devices[0].ip == "192.168.1.1"
