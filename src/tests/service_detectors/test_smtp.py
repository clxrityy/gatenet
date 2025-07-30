from gatenet.service_detectors.smtp import SMTPDetector
import pytest

def test_smtp_detector_postfix():
    detector = SMTPDetector()
    result = detector.detect(25, "220 mail.example.com esmtp postfix")
    assert result == "Postfix SMTP"

def test_smtp_detector_sendmail():
    detector = SMTPDetector()
    result = detector.detect(25, "220 mail.example.com esmtp sendmail")
    assert result == "Sendmail SMTP"

def test_smtp_detector_generic():
    detector = SMTPDetector()
    result = detector.detect(25, "220 mail.example.com esmtp smtp")
    assert result == "SMTP Server"

def test_smtp_detector_non_smtp():
    detector = SMTPDetector()
    result = detector.detect(80, "http/1.1 200 ok")
    assert result is None
