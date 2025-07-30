from gatenet.service_detectors.http import HTTPDetector
import pytest

def test_http_detector_apache():
    detector = HTTPDetector()
    result = detector.detect(80, "apache/2.4.41")
    assert result == "Apache HTTP Server"

def test_http_detector_nginx():
    detector = HTTPDetector()
    result = detector.detect(443, "nginx/1.18.0")
    assert result == "Nginx HTTP Server"

def test_http_detector_iis():
    detector = HTTPDetector()
    result = detector.detect(80, "microsoft-iis/10.0")
    assert result == "Microsoft IIS"

def test_http_detector_generic():
    detector = HTTPDetector()
    result = detector.detect(8080, "http/1.1 200 ok")
    assert result == "HTTP Server"

def test_http_detector_non_http():
    detector = HTTPDetector()
    result = detector.detect(22, "ssh-2.0-openssh")
    assert result is None
