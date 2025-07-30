from gatenet.service_detectors.banner_keyword import BannerKeywordDetector
import pytest

def test_banner_keyword_telnet():
    detector = BannerKeywordDetector()
    result = detector.detect(23, "welcome to telnet server")
    assert result == "Telnet Server"

def test_banner_keyword_pop3():
    detector = BannerKeywordDetector()
    result = detector.detect(110, "+OK pop3 server ready")
    assert result == "POP3 Server"

def test_banner_keyword_imap():
    detector = BannerKeywordDetector()
    result = detector.detect(143, "* OK imap4rev1 service ready")
    assert result == "IMAP Server"

def test_banner_keyword_none():
    detector = BannerKeywordDetector()
    result = detector.detect(80, "http/1.1 200 ok")
    assert result is None
