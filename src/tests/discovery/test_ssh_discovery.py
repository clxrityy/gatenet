from gatenet.discovery.ssh import (
    SSHDetector, HTTPDetector, FTPDetector, SMTPDetector,
    PortMappingDetector, BannerKeywordDetector, GenericServiceDetector,
    _identify_service
)

def test_ssh_detector():
    """Test SSH service detection."""
    detector = SSHDetector()
    
    # Test OpenSSH detection with lowercase (as expected by implementation)
    result = detector.detect(22, "ssh-2.0-openssh_8.9p1")
    assert result == "OpenSSH 8.9p1"
    
    # Test generic SSH detection
    result = detector.detect(22, "ssh-2.0-somessh")
    assert result == "SSH Server"
    
    # Test non-SSH port with SSH banner
    result = detector.detect(2222, "ssh-2.0-openssh_7.4")
    assert result == "OpenSSH 7.4"
    
    # Test non-SSH service
    result = detector.detect(80, "http/1.1 200 ok")
    assert result is None
    
    # Test SSH port but no SSH banner
    result = detector.detect(22, "http/1.1 200 ok")
    assert result is None

def test_http_detector():
    """Test HTTP service detection."""
    detector = HTTPDetector()
    
    # Test Apache detection (lowercase as expected)
    result = detector.detect(80, "apache/2.4.41")
    assert result == "Apache HTTP Server"
    
    # Test Nginx detection
    result = detector.detect(443, "nginx/1.18.0")
    assert result == "Nginx HTTP Server"
    
    # Test IIS detection
    result = detector.detect(80, "microsoft-iis/10.0")
    assert result == "Microsoft IIS"
    
    # Test generic HTTP
    result = detector.detect(8080, "http/1.1 200 ok")
    assert result == "HTTP Server"
    
    # Test non-HTTP service
    result = detector.detect(22, "ssh-2.0-openssh")
    assert result is None

def test_ftp_detector():
    """Test FTP service detection."""
    detector = FTPDetector()
    
    # Test vsftpd detection
    result = detector.detect(21, "220 (vsftpd 3.0.3)")
    assert result == "vsftpd FTP Server"
    
    # Test FileZilla detection
    result = detector.detect(21, "220-filezilla server 0.9.60")
    assert result == "FileZilla FTP Server"
    
    # Test generic FTP
    result = detector.detect(21, "220 ftp server ready")
    assert result == "FTP Server"
    
    # Test non-FTP service
    result = detector.detect(80, "http/1.1 200 ok")
    assert result is None

def test_smtp_detector():
    """Test SMTP service detection."""
    detector = SMTPDetector()
    
    # Test Postfix detection
    result = detector.detect(25, "220 mail.example.com esmtp postfix")
    assert result == "Postfix SMTP"
    
    # Test Sendmail detection
    result = detector.detect(25, "220 mail.example.com esmtp sendmail")
    assert result == "Sendmail SMTP"
    
    # Test generic SMTP
    result = detector.detect(25, "220 smtp ready")
    assert result == "SMTP Server"
    
    # Test non-SMTP service
    result = detector.detect(80, "http/1.1 200 ok")
    assert result is None

def test_port_mapping_detector():
    """Test port-based service detection."""
    detector = PortMappingDetector()
    
    # Test HTTPS detection
    result = detector.detect(443, "")
    assert result == "HTTPS Server"
    
    # Test DNS detection
    result = detector.detect(53, "")
    assert result == "DNS Server"
    
    # Test Telnet detection
    result = detector.detect(23, "")
    assert result == "Telnet Server"
    
    # Test POP3 detection
    result = detector.detect(110, "")
    assert result == "POP3 Server"
    
    # Test IMAP detection
    result = detector.detect(143, "")
    assert result == "IMAP Server"
    
    # Test RDP detection
    result = detector.detect(3389, "")
    assert result == "Remote Desktop Protocol (RDP)"
    
    # Test unknown port
    result = detector.detect(9999, "")
    assert result is None

def test_banner_keyword_detector():
    """Test banner keyword-based service detection."""
    detector = BannerKeywordDetector()
    
    # Test telnet keyword detection
    result = detector.detect(23, "telnet service ready")
    assert result == "Telnet Server"
    
    # Test POP3 keyword detection
    result = detector.detect(110, "+ok pop3 server ready")
    assert result == "POP3 Server"
    
    # Test IMAP keyword detection
    result = detector.detect(143, "* ok imap4rev1 ready")
    assert result == "IMAP Server"
    
    # Test no keyword match
    result = detector.detect(80, "http/1.1 200 ok")
    assert result is None

def test_generic_service_detector():
    """Test generic service detection by banner keywords."""
    detector = GenericServiceDetector()
    
    # Test MySQL detection
    result = detector.detect(3306, "mysql server ready")
    assert result == "MySQL Database"
    
    # Test PostgreSQL detection
    result = detector.detect(5432, "postgresql 13.3 ready")
    assert result == "PostgreSQL Database"
    
    # Test Redis detection
    result = detector.detect(6379, "redis server v6.0")
    assert result == "Redis Server"
    
    # Test MongoDB detection
    result = detector.detect(27017, "mongodb 4.4.8")
    assert result == "MongoDB Database"
    
    # Test Elasticsearch detection
    result = detector.detect(9200, "elasticsearch cluster")
    assert result == "Elasticsearch"
    
    # Test Jenkins detection
    result = detector.detect(8080, "jenkins automation server")
    assert result == "Jenkins CI/CD"
    
    # Test GitLab detection
    result = detector.detect(80, "gitlab community edition")
    assert result == "GitLab"
    
    # Test Docker detection
    result = detector.detect(5000, "docker registry api")
    assert result == "Docker Registry"
    
    # Test unknown service
    result = detector.detect(1234, "unknown service")
    assert result is None

def test_service_identification_integration():
    """Test the main service identification function."""
    
    # Test SSH identification (case insensitive)
    result = _identify_service(22, "SSH-2.0-OpenSSH_8.9p1")
    assert result == "OpenSSH 8.9p1"
    
    # Test HTTP identification (case insensitive)
    result = _identify_service(80, "Apache/2.4.41")
    assert result == "Apache HTTP Server"
    
    # Test port mapping fallback
    result = _identify_service(443, "")
    assert result == "HTTPS Server"
    
    # Test generic service detection
    result = _identify_service(3306, "MySQL Server 8.0")
    assert result == "MySQL Database"
    
    # Test fallback for unknown service with banner
    result = _identify_service(9999, "unknown banner")
    assert result == "Unknown Service (Port 9999)"
    
    # Test fallback for unknown service without banner
    result = _identify_service(12345, "")
    assert result == "Unknown Service (Port 12345)"

def test_service_identification_case_insensitive():
    """Test that service identification handles case correctly."""
    
    # Test SSH with mixed case
    result = _identify_service(22, "SSH-2.0-OPENSSH_8.9P1")
    assert result == "OpenSSH 8.9p1"
    
    # Test HTTP with mixed case
    result = _identify_service(80, "SERVER: APACHE/2.4.41")
    assert result == "Apache HTTP Server"
    
    # Test Nginx with mixed case
    result = _identify_service(80, "SERVER: NGINX/1.18.0")
    assert result == "Nginx HTTP Server"

def test_service_identification_whitespace_handling():
    """Test proper handling of whitespace in banners."""
    
    # Test SSH with extra whitespace
    result = _identify_service(22, "  SSH-2.0-OpenSSH_8.9p1  \r\n")
    assert result == "OpenSSH 8.9p1"
    
    # Test HTTP with extra whitespace
    result = _identify_service(80, "\tServer: Apache/2.4.41\r\n")
    assert result == "Apache HTTP Server"

def test_service_identification_port_override():
    """Test that banner content can override port-based identification."""
    
    # Test SSH on non-standard port
    result = _identify_service(2222, "SSH-2.0-OpenSSH_8.9")
    assert result == "OpenSSH 8.9"
    
    # Test HTTP on non-standard port
    result = _identify_service(8888, "HTTP/1.1 200 OK\nServer: nginx")
    assert result == "Nginx HTTP Server"
    
    # Test FTP on non-standard port
    result = _identify_service(2121, "220 (vsFTPd 3.0.3)")
    assert result == "vsftpd FTP Server"

def test_service_identification_detector_chain():
    """Test that the detector chain works correctly."""
    
    # Test that first matching detector wins
    banner_with_multiple_indicators = "ssh-2.0-openssh_8.9 running on apache server"
    result = _identify_service(22, banner_with_multiple_indicators)
    
    # Should match SSH detector first, not Apache/HTTP detector
    assert result == "OpenSSH 8.9"
    assert "Apache" not in result

def test_fallback_detector_always_returns_result():
    """Test that service identification always returns a result."""
    
    # Test various edge cases
    result1 = _identify_service(99999, "")
    result2 = _identify_service(0, "random banner")
    result3 = _identify_service(-1, "")
    
    assert isinstance(result1, str)
    assert isinstance(result2, str)
    assert isinstance(result3, str)
    assert all("Unknown Service" in r for r in [result1, result2, result3])