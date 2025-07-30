from gatenet.service_detectors.port_mapping import PortMappingDetector
import pytest

def test_port_mapping_known_ports():
    detector = PortMappingDetector()
    assert detector.detect(443, "") == "HTTPS Server"
    assert detector.detect(53, "") == "DNS Server"
    assert detector.detect(23, "") == "Telnet Server"
    assert detector.detect(110, "") == "POP3 Server"
    assert detector.detect(3389, "") == "Remote Desktop Protocol (RDP)"

def test_port_mapping_unknown_port():
    detector = PortMappingDetector()
    assert detector.detect(9999, "") is None
