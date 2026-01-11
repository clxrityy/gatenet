from gatenet.scan.ports import scan_target


def test_scan_target_basic():
    result = scan_target("localhost", ports=[22, 80])
    assert result.target == "localhost"
    assert result.open_ports is not None
    open_port_numbers = [port.number for port in result.open_ports]
    if open_port_numbers:
        # Check that at least one of the common ports is closed
        assert all(port in open_port_numbers for port in [22, 80]) is False
    else:
        # No open ports found
        assert open_port_numbers == []
