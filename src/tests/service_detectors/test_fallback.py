from gatenet.service_detectors.fallback import FallbackDetector
import pytest

def test_fallback_known_ports():
    detector = FallbackDetector()
    assert detector.detect(22, "") == "SSH"
    assert detector.detect(80, "") == "HTTP"
    assert detector.detect(443, "") == "HTTPS"
    assert detector.detect(21, "") == "FTP"
    assert detector.detect(3389, "") == "RDP"

def test_fallback_unknown_port():
    detector = FallbackDetector()
    assert detector.detect(9999, "") == "Unknown Service (Port 9999)"

def test_fallback_with_banner():
    detector = FallbackDetector()
    assert detector.detect(22, "some banner") == "Unknown Service (Port 22)"
