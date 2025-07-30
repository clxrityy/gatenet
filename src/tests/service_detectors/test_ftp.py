from gatenet.service_detectors.ftp import FTPDetector
import pytest

def test_ftp_detector_vsftpd():
    detector = FTPDetector()
    result = detector.detect(21, "220 (vsftpd 3.0.3)")
    assert result == "vsftpd FTP Server"

def test_ftp_detector_filezilla():
    detector = FTPDetector()
    result = detector.detect(21, "220-filezilla server 0.9.60")
    assert result == "FileZilla FTP Server"

def test_ftp_detector_generic():
    detector = FTPDetector()
    result = detector.detect(21, "220 ftp server ready")
    assert result == "FTP Server"

def test_ftp_detector_non_ftp():
    detector = FTPDetector()
    result = detector.detect(80, "http/1.1 200 ok")
    assert result is None
