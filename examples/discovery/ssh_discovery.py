#!/usr/bin/env python3
"""
Example usage of the Gatenet service discovery module.

This example demonstrates how to use the service detection functionality
to identify services running on network hosts by analyzing banners and ports.
"""

NGINX_BANNER = "Server: nginx/1.18.0"
SSH_OPENSSH_BANNER = "SSH-2.0-OpenSSH_8.9p1"

import asyncio
from typing import Optional
from gatenet.discovery.ssh import (
    _identify_service,
    SSHDetector,
    HTTPDetector,
    FTPDetector,
    SMTPDetector,
    PortMappingDetector,
    BannerKeywordDetector,
    GenericServiceDetector,
    FallbackDetector,
    ServiceDetector
)


def basic_service_identification():
    """Demonstrate basic service identification from port and banner."""
    print("=== Basic Service Identification ===")
    
    # Example service banners you might encounter
    services = [
        (22, f"{SSH_OPENSSH_BANNER} Ubuntu-3ubuntu0.1"),
        (80, "HTTP/1.1 200 OK\nServer: nginx/1.18.0"),
        (21, "220 (vsFTPd 3.0.3)"),
        (25, "220 mail.example.com ESMTP Postfix"),
        (443, ""),  # HTTPS on standard port, no banner
        (3306, "MySQL Server 8.0.25"),
        (9999, "CustomApp v1.0"),  # Unknown service
    ]
    
    for port, banner in services:
        service = _identify_service(port, banner)
        print(f"Port {port:4d}: {service}")
        if banner:
            print(f"         Banner: {banner[:50]}{'...' if len(banner) > 50 else ''}")
        print()

def individual_detector_examples():
    """Demonstrate using individual detector classes."""
    print("=== Individual Detector Examples ===")
    
    # SSH Detection
    ssh_detector = SSHDetector()
    print("SSH Detector:")
    ssh_banners = [
        SSH_OPENSSH_BANNER,
        "SSH-2.0-libssh_0.8.9",
        "HTTP/1.1 200 OK"  # Non-SSH
    ]
    
    for banner in ssh_banners:
        result = ssh_detector.detect(22, banner.lower())
        print(f"  {banner:25} -> {result}")
    print()
    
    # HTTP Detection
    http_detector = HTTPDetector()
    http_banners = [
        "Server: Apache/2.4.41",
        NGINX_BANNER, 
        "Server: Microsoft-IIS/10.0",
        "HTTP/1.1 200 OK"
    ]
    
    for banner in http_banners:
        result = http_detector.detect(80, banner.lower())
        print(f"  {banner:25} -> {result}")
    print()
    
    # Port Mapping Detection
    port_detector = PortMappingDetector()
    print("Port Mapping Detector:")
    well_known_ports = [443, 53, 23, 110, 3389, 9999]
    
    for port in well_known_ports:
        result = port_detector.detect(port, "")
        print(f"  Port {port:4d}               -> {result}")
    print()


def service_discovery_chain():
    """Demonstrate the chain of responsibility pattern."""
    print("=== Service Discovery Chain ===")
    
    # Create all detectors in order
    detectors = [
        ("SSH", SSHDetector()),
        ("HTTP", HTTPDetector()),
        ("FTP", FTPDetector()),
        ("SMTP", SMTPDetector()),
        ("Port Mapping", PortMappingDetector()),
        ("Banner Keywords", BannerKeywordDetector()),
        ("Generic Service", GenericServiceDetector()),
        ("Fallback", FallbackDetector())
    ]
    test_cases = [
        (22, SSH_OPENSSH_BANNER.lower() + " running on apache server"),
        (80, "nginx/1.18.0 with mysql backend"),
        (9999, "telnet interface for custom app"),
        (12345, "")  # Unknown service, no banner
    ]
    
    for port, banner in test_cases:
        print(f"Testing port {port} with banner: '{banner}'")
        banner_lower = banner.lower().strip()
        
        for name, detector in detectors:
            result = detector.detect(port, banner_lower)
            status = "✓ MATCH" if result else "✗ No match"
            print(f"  {name:15} -> {status:10} {result or ''}")
            if result:  # Stop at first match (chain of responsibility)
                break
        print()


def practical_examples():
    """Show practical usage scenarios."""
    print("=== Practical Usage Scenarios ===")
    
    web_services = [
        (80, "Server: Apache/2.4.41 (Ubuntu)"),
        (443, "Server: Apache/2.4.41 (Ubuntu)"),
        (8080, NGINX_BANNER),
        (3000, "Express.js application")
    ]
    
    for port, banner in web_services:
        service = _identify_service(port, banner)
        print(f"   Port {port}: {service}")
    print()
    
    # Scenario 2: Database server identification
    print("2. Database Server Analysis:")
    db_services = [
        (3306, "MySQL Server 8.0.25"),
        (5432, "PostgreSQL 13.3 on Linux"),
        (6379, "Redis server v=6.2.6"),
        (27017, "MongoDB shell version v4.4.8"),
        (1433, "Microsoft SQL Server 2019")
    ]
    
    for port, banner in db_services:
        service = _identify_service(port, banner)
        print(f"   Port {port}: {service}")
    print()
    
    mixed_services = [
        (22, SSH_OPENSSH_BANNER),
        (25, "220 Postfix SMTP server"),
        (53, ""),  # DNS, identified by port
        (80, NGINX_BANNER),
        (143, "* OK IMAP4rev1 ready"),
        (443, ""),  # HTTPS, identified by port
        (993, ""),  # IMAPS, identified by port
        (8080, "Jenkins/2.401.3")
    ]
    
    for port, banner in mixed_services:
        service = _identify_service(port, banner)
        security_note = ""
        if "SSH" in service and "OpenSSH" in service:
            security_note = " (Check for updates)"
        elif port in [23, 21] and "Server" in service:
            security_note = " (Consider secure alternatives)"
        
        print(f"   Port {port:4d}: {service}{security_note}")
    print()


def case_sensitivity_demo():
    """Demonstrate case-insensitive detection."""
    test_cases = [
        (22, SSH_OPENSSH_BANNER.upper()),  # Uppercase
        (22, SSH_OPENSSH_BANNER.lower()),  # Lowercase
        (80, "SERVER: APACHE/2.4.41"),   # Mixed case
        (80, "server: nginx/1.18.0"),    # Lowercase
    ]
    
    for port, banner in test_cases:
        service = _identify_service(port, banner)
        print(f"Banner: {banner:30} -> {service}")
    print()


def custom_detector_example():
    """Show how to create a custom detector."""
    print("=== Custom Detector Example ===")
    
    class CustomAppDetector(ServiceDetector):
        """Detects custom application services."""
        
        def detect(self, port: int, banner: str) -> Optional[str]:
            """Detect custom application from banner."""
            if 'myapp' in banner:
                if 'v1.0' in banner:
                    return "MyApp v1.0"
                elif 'v2.0' in banner:
                    return "MyApp v2.0"
                else:
                    return "MyApp (unknown version)"
            return None
    
    # Test the custom detector
    custom_detector = CustomAppDetector()
    
    test_banners = [
        "MyApp v1.0 HTTP Server",
        "MyApp v2.0 with SSL",
        "MyApp beta build",
        "Apache HTTP Server"  # Should not match
    ]
    
    print("Custom App Detector Results:")
    for banner in test_banners:
        result = custom_detector.detect(8080, banner.lower())
        print(f"  {banner:25} -> {result}")
    print()


async def async_usage_example():
    """Demonstrate usage in async context (for future async discovery)."""
    print("=== Async Usage Example ===")
    
    # Simulate async service discovery results
    async def simulate_banner_grab(port: int) -> tuple[int, str]:
        """Simulate grabbing a banner from a service."""
        await asyncio.sleep(0.1)  # Simulate network delay
        
        # Mock responses based on port
        mock_responses = {
            22: SSH_OPENSSH_BANNER,
            80: "Server: nginx/1.18.0",
            443: "",
            25: "220 Postfix SMTP"
        }
        return port, mock_responses.get(port, "")
    
    # Simulate scanning multiple ports
    host = "example.com"
    ports = [22, 80, 443, 25, 3306]
    
    print(f"Scanning {host}...")
    
    # Gather results concurrently
    tasks = [simulate_banner_grab(port) for port in ports]
    results = await asyncio.gather(*tasks)
    
    print("Results:")
    for port, banner in results:
        service = _identify_service(port, banner)
        status = "Open" if banner or port in [443, 53] else "Filtered/Closed"
        print(f"  {host}:{port:4d} -> {service:20} [{status}]")
    print()


def main():
    """Run all examples."""
    print("Gatenet Service Discovery Examples")
    print("=" * 50)
    print()
    
    # Run synchronous examples
    basic_service_identification()
    individual_detector_examples()
    service_discovery_chain()
    practical_examples()
    case_sensitivity_demo()
    custom_detector_example()
    
    # Run async example
    print("Running async example...")
    asyncio.run(async_usage_example())
    
    print("Examples completed!")


if __name__ == "__main__":
    main()
    
# EXPECTED OUTPUT:
"""
Gatenet Service Discovery Examples
==================================================

=== Basic Service Identification ===
Port   22: OpenSSH 8.9p1
         Banner: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1

Port   80: Nginx HTTP Server
         Banner: HTTP/1.1 200 OK
Server: nginx/1.18.0

Port   21: vsftpd FTP Server
         Banner: 220 (vsFTPd 3.0.3)

Port   25: Postfix SMTP
         Banner: 220 mail.example.com ESMTP Postfix

Port  443: HTTPS Server

Port 3306: MySQL Database
         Banner: MySQL Server 8.0.25

Port 9999: Unknown Service (Port 9999)
         Banner: CustomApp v1.0

=== Individual Detector Examples ===
SSH Detector:
  SSH-2.0-OpenSSH_8.9p1     -> OpenSSH 8.9p1
  SSH-2.0-libssh_0.8.9      -> SSH Server
  HTTP/1.1 200 OK           -> None

HTTP Detector:
  Server: Apache/2.4.41     -> Apache HTTP Server
  Server: nginx/1.18.0      -> Nginx HTTP Server
  Server: Microsoft-IIS/10.0 -> Microsoft IIS
  HTTP/1.1 200 OK           -> HTTP Server

Port Mapping Detector:
  Port  443               -> HTTPS Server
  Port   53               -> DNS Server
  Port   23               -> Telnet Server
  Port  110               -> POP3 Server
  Port 3389               -> Remote Desktop Protocol (RDP)
  Port 9999               -> None

=== Service Discovery Chain ===
Testing port 22 with banner: 'ssh-2.0-openssh_8.9p1 running on apache server'
  SSH             -> ✓ MATCH    OpenSSH 8.9p1

Testing port 80 with banner: 'nginx/1.18.0 with mysql backend'
  SSH             -> ✗ No match 
  HTTP            -> ✓ MATCH    Nginx HTTP Server

Testing port 9999 with banner: 'telnet interface for custom app'
  SSH             -> ✗ No match 
  HTTP            -> ✗ No match 
  FTP             -> ✗ No match 
  SMTP            -> ✗ No match 
  Port Mapping    -> ✗ No match 
  Banner Keywords -> ✓ MATCH    Telnet Server

Testing port 12345 with banner: ''
  SSH             -> ✗ No match 
  HTTP            -> ✗ No match 
  FTP             -> ✗ No match 
  SMTP            -> ✗ No match 
  Port Mapping    -> ✗ No match 
  Banner Keywords -> ✗ No match 
  Generic Service -> ✗ No match 
  Fallback        -> ✓ MATCH    Unknown Service (Port 12345)

=== Practical Usage Scenarios ===
   Port 80: Apache HTTP Server
   Port 443: Apache HTTP Server
   Port 8080: Nginx HTTP Server
   Port 3000: Unknown Service (Port 3000)

2. Database Server Analysis:
   Port 3306: MySQL Database
   Port 5432: PostgreSQL Database
   Port 6379: Redis Server
   Port 27017: MongoDB Database
   Port 1433: Unknown Service (Port 1433)

   Port   22: OpenSSH 8.9p1 (Check for updates)
   Port   25: Postfix SMTP
   Port   53: DNS Server
   Port   80: Nginx HTTP Server
   Port  143: IMAP Server
   Port  443: HTTPS Server
   Port  993: IMAPS Server
   Port 8080: Jenkins CI/CD

Banner: SSH-2.0-OPENSSH_8.9P1          -> OpenSSH 8.9p1
Banner: ssh-2.0-openssh_8.9p1          -> OpenSSH 8.9p1
Banner: SERVER: APACHE/2.4.41          -> Apache HTTP Server
Banner: server: nginx/1.18.0           -> Nginx HTTP Server

=== Custom Detector Example ===
Custom App Detector Results:
  MyApp v1.0 HTTP Server   -> MyApp v1.0
  MyApp v2.0 with SSL      -> MyApp v2.0
  MyApp beta build         -> MyApp (unknown version)
  Apache HTTP Server       -> None

=== Async Usage Example ===
Scanning example.com...
Results:
  example.com:  22 -> OpenSSH 8.9p1       [Open]
  example.com:  80 -> Nginx HTTP Server   [Open]
  example.com: 443 -> HTTPS Server        [Open]
  example.com:  25 -> Postfix SMTP        [Open]
  example.com:3306 -> Unknown Service (Port 3306) [Filtered/Closed]

Examples completed!
"""