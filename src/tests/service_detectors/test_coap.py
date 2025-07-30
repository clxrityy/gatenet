import pytest
from gatenet.service_detectors.coap import CoAPDetector

@pytest.mark.parametrize("port,banner,expected", [
    (5683, "CoAP Server Ready", "CoAP Server"),
    (5683, "coap", "CoAP Server"),
    (80, "coap", "CoAP Server"),
    (5683, "", None),
    (80, "", None),
])
def test_coap_detector(port, banner, expected):
    detector = CoAPDetector()
    assert detector.detect(port, banner) == expected
