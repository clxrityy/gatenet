from gatenet.scan.ports import scan_target


def test_scan_target_basic():
    result = scan_target("example.com")
    assert result.target == "example.com"
    assert len(result.open_ports) == 2
    port_numbers = [port.number for port in result.open_ports]
    assert 22 in port_numbers
    assert 80 in port_numbers
    services = [port.service for port in result.open_ports]
    assert "ssh" in services
    assert "http" in services
