from gatenet.utils import COMMON_PORTS

def test_common_ports():
    """
    Test that COMMON_PORTS contains expected ports.
    """
    expected_port = 21
    
    assert expected_port in COMMON_PORTS, f"Expected port {expected_port} not found in COMMON_PORTS"