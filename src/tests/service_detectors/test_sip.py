import pytest
from gatenet.service_detectors.sip import SIPDetector

@pytest.mark.parametrize("port,banner,expected", [
    (5060, "SIP/2.0 200 OK", "SIP Server"),
    (5060, "sip", "SIP Server"),
    (80, "sip", "SIP Server"),
    (5060, "", None),
    (80, "", None),
])
def test_sip_detector(port, banner, expected):
    detector = SIPDetector()
    assert detector.detect(port, banner) == expected
