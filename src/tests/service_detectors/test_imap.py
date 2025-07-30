import pytest
from gatenet.service_detectors.imap import IMAPDetector

@pytest.mark.parametrize("port,banner,expected", [
    (143, "IMAP4rev1 Service Ready", "IMAP Server"),
    (993, "IMAPS Service Ready", "IMAPS Server"),
    (143, "Welcome to imap.example.com", "IMAP Server"),
    (993, "imaps", "IMAPS Server"),
    (143, "", None),
    (80, "", None),
    (993, "", "IMAPS Server"),
    (143, "random banner", None),
])
def test_imap_detector(port, banner, expected):
    detector = IMAPDetector()
    assert detector.detect(port, banner) == expected
