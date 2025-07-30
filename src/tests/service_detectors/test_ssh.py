from gatenet.service_detectors.ssh import SSHDetector, ServiceDetector
import pytest

def test_ssh_detector_openssh():
    detector = SSHDetector()
    result = detector.detect(22, "ssh-2.0-openssh_8.9p1")
    assert result == "OpenSSH 8.9p1"

def test_ssh_detector_generic():
    detector = SSHDetector()
    result = detector.detect(22, "ssh-2.0-somessh")
    assert result == "SSH Server"

def test_ssh_detector_non_ssh_port():
    detector = SSHDetector()
    result = detector.detect(2222, "ssh-2.0-openssh_7.4")
    assert result == "OpenSSH 7.4"

def test_ssh_detector_non_ssh_service():
    detector = SSHDetector()
    result = detector.detect(80, "http/1.1 200 ok")
    assert result is None

def test_ssh_detector_ssh_port_no_banner():
    detector = SSHDetector()
    result = detector.detect(22, "http/1.1 200 ok")
    assert result is None
