from gatenet.service_detectors.generic import GenericServiceDetector
import pytest

def test_generic_mysql():
    detector = GenericServiceDetector()
    result = detector.detect(3306, "mysql server ready")
    assert result == "MySQL Database"

def test_generic_postgresql():
    detector = GenericServiceDetector()
    result = detector.detect(5432, "postgresql 13.3")
    assert result == "PostgreSQL Database"

def test_generic_redis():
    detector = GenericServiceDetector()
    result = detector.detect(6379, "redis v6.2.5")
    assert result == "Redis Server"

def test_generic_none():
    detector = GenericServiceDetector()
    result = detector.detect(80, "http/1.1 200 ok")
    assert result is None
