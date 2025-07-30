import pytest
from gatenet.service_detectors.pop3 import POP3Detector

@pytest.mark.parametrize("port,banner,expected", [
    (110, "+OK POP3 server ready", "POP3 Server"),
    (995, "+OK POP3S server ready", "POP3S Server"),
    (110, "pop3", "POP3 Server"),
    (995, "pop3s", "POP3S Server"),
    (110, "", "POP3 Server"),
    (995, "", "POP3S Server"),
    (143, "", None),
    (995, "random banner", "POP3S Server"),
])
def test_pop3_detector(port, banner, expected):
    detector = POP3Detector()
    assert detector.detect(port, banner) == expected
