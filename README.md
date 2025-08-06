# gatenet 🛰️

[![PyPI](https://img.shields.io/pypi/v/gatenet?style=for-the-badge)](https://pypi.org/project/gatenet/)

[![Static Badge](https://img.shields.io/badge/readthedocs-readme?style=for-the-badge&logo=readthedocs&logoColor=%23182026&color=%23788793&link=https%3A%2F%2Fgatenet.readthedocs.io%2Fen%2Flatest%2F)](https://gatenet.readthedocs.io/en/latest/) [![Changelog](https://img.shields.io/badge/changelog-log?logo=gitbook&logoColor=%23333333&color=%233860a9&style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fclxrityy%2Fgatenet%2Fblob%2Fmaster%2FCHANGELOG.md)](https://gatenet.readthedocs.io/en/latest/changelog.html)

> Gatenet is a comprehensive Python networking toolkit for diagnostics, service discovery, hotspot management, mesh networking, and building robust microservices with TCP/UDP/HTTP and radio capabilities.

[![CI](https://github.com/clxrityy/gatenet/actions/workflows/test.yml/badge.svg?style=for-the-badge)](https://github.com/clxrityy/gatenet/actions/workflows/test.yml) [![codecov](https://codecov.io/gh/clxrityy/gatenet/graph/badge.svg?token=4644O5NGW9&style=for-the-badge)](https://codecov.io/gh/clxrityy/gatenet)

# 🔗 Resources

- [📚 Documentation](https://gatenet.readthedocs.io/en/latest/) - Complete guides and API reference
- [🎮 Interactive Sandbox](https://gatenet.readthedocs.io/en/latest/sandbox.html) - Try Gatenet in your browser
- [📖 Changelog](https://gatenet.readthedocs.io/en/latest/changelog.html) - Latest features and updates
- [⚡ Quick Start](#-quick-start)
- [🚀 Core Features](#-core-features)
- [💻 Code Examples](#-code-examples)
- [📡 Hotspot Management](#-hotspot-management)
- [🔍 Service Discovery](#-service-discovery)
- [🧪 Testing & Development](#-testing--development)

**Perfect for network engineers, security researchers, IoT developers, and anyone building network-aware applications.**

---

## 📦 Installation

```bash
pip install gatenet
```

**Requirements:** Python 3+ • Cross-platform (Linux, macOS, Windows)

---

## 🚀 Core Features

- [Network Diagnostics](#network-diagnostics)
- [Hotspot Management](#hotspot-management)
- [Microservice Framework](#microservice-framework)
- [Advanced Networking](#advanced-networking)

### 🔧 **Network Diagnostics**

- **Smart Ping:** ICMP and TCP ping with jitter analysis and packet loss statistics
- **Advanced Traceroute:** Multi-protocol route tracing with hop-by-hop analysis
- **Bandwidth Testing:** Real-time upload/download speed measurement
- **Port Scanner:** Fast async port scanning with service detection
- **DNS Tools:** Forward/reverse lookups with comprehensive error handling
- **Geo Location:** IP geolocation with ISP and organization data

### 📡 **Hotspot Management** (`v0.12.0`)

- **Cross-Platform AP Creation:** Linux (hostapd) and macOS (Internet Sharing) support
- **Advanced Security:** WPA2, WPA3, WEP, and open network configurations
- **DHCP Integration:** Automatic IP assignment with configurable ranges
- **Device Monitoring:** Real-time connected device tracking
- **Password Management:** Secure password generation with complexity validation

### 🌐 **Microservice Framework**

- **Production HTTP Servers:** FastAPI-based with automatic JSON handling
- **Robust TCP/UDP:** Connection pooling, timeouts, and retry logic
- **Full Async Support:** Native asyncio integration for high-performance apps
- **Middleware System:** Extensible request/response processing
- **Health Monitoring:** Built-in health checks and metrics collection

### 🛰️ **Advanced Networking**

- **Mesh Networks:** Self-healing topology with encrypted communication
- **Radio Integration:** LoRa, ESP, and SDR hardware support
- **GPS Tracking:** Location-aware network operations
- **Protocol Extension:** Plugin architecture for custom protocols

---

## ⚡ Quick Start

- [HTTP Microservice](#-http-microservice)
- [Hotspot Creation](#-hotspot-creation)
- [Smart Service Discovery](#-smart-service-discovery)
- [Network Diagnostics](#-network-diagnostics)

### 🌐 HTTP Microservice

```python
from gatenet.http_.server import HTTPServer

app = HTTPServer(host="0.0.0.0", port=8080)

@app.route("/api/health", method="GET")
def health_check(request):
    return {"status": "healthy", "service": "gatenet-api"}

@app.route("/api/ping", method="POST")
def ping_service(request):
    from gatenet.diagnostics.ping import ping
    host = request.json.get("host", "8.8.8.8")
    result = ping(host, count=3)
    return {"host": host, "result": result}

if __name__ == "__main__":
    app.serve()  # Production-ready server
```

### 📡 Hotspot Creation

```python
from gatenet.hotspot import Hotspot, SecurityConfig

# Create a secure WPA2 hotspot
security = SecurityConfig(
    security_type="WPA2",
    password="MySecureNetwork123!"  # Or auto-generate
)

hotspot = Hotspot(
    ssid="GatenetAP",
    interface="wlan0",  # Linux: wlan0, macOS: en0
    security=security
)

# Start the access point
if hotspot.start():
    print(f"Hotspot '{hotspot.ssid}' is running!")
    print(f"Connected devices: {hotspot.get_connected_devices()}")

    # Stop when done
    # hotspot.stop()
```

### 🔍 Smart Service Discovery

```python
from gatenet.discovery.ssh import _identify_service
from gatenet.discovery.service_discovery import ServiceDiscovery

# Quick service identification
service = _identify_service(22, "SSH-2.0-OpenSSH_8.9p1")
print(f"Detected: {service}")  # "OpenSSH 8.9p1"

# Advanced discovery with multiple detectors
discovery = ServiceDiscovery()
discovery.add_detector("http").add_detector("ssh").add_detector("ftp")

result = discovery.identify_service(80, "nginx/1.18.0 (Ubuntu)")
print(f"Service: {result}")  # "Nginx Web Server"
```

### 🛰️ Network Diagnostics

```python
from gatenet.diagnostics import ping, traceroute, scan_ports

# Advanced ping with statistics
result = ping("google.com", count=5, timeout=3)
print(f"Average RTT: {result['avg_rtt']}ms")
print(f"Packet Loss: {result['packet_loss']}%")
print(f"Jitter: {result['jitter']}ms")

# Traceroute with hop analysis
hops = traceroute("github.com", max_hops=15)
for i, hop in enumerate(hops, 1):
    print(f"Hop {i}: {hop['ip']} ({hop['hostname']}) - {hop['rtt']}ms")

# Fast async port scanning
open_ports = scan_ports("192.168.1.1", [22, 80, 443, 8080])
print(f"Open ports: {open_ports}")
```

---

## 💻 Code Examples

- [Async TCP Client](#-async-tcp-client)
- [Production HTTP Client](#-production-http-client)
- [Advanced Hotspot Configuration](#-advanced-hotspot-configuration)

### 🔧 **Async TCP Client**

```python
import asyncio
from gatenet.client.tcp import AsyncTCPClient

async def tcp_example():
    client = AsyncTCPClient("127.0.0.1", 8080, timeout=10)

    try:
        await client.connect()
        response = await client.send("Hello Server!")
        print(f"Server response: {response}")
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        await client.close()

asyncio.run(tcp_example())
```

### 🌐 **Production HTTP Client**

```python
from gatenet.http_.client import HTTPClient

# RESTful API client with automatic retry
client = HTTPClient(
    base_url="https://api.example.com",
    timeout=30,
    retries=3
)

# GET with custom headers
response = client.get("/users/123", headers={
    "Authorization": "Bearer token123",
    "User-Agent": "Gatenet/1.0"
})

# POST with JSON payload
user_data = {"name": "Alice", "email": "alice@example.com"}
response = client.post("/users", json=user_data)

print(f"Status: {response['status']}")
print(f"Data: {response['data']}")
```

### 📡 **Advanced Hotspot Configuration**

```python
from gatenet.hotspot import Hotspot, SecurityConfig, DHCPServer

# Enterprise-grade hotspot setup
security = SecurityConfig.generate_secure_config(
    security_type="WPA3",
    password_length=16  # Auto-generated secure password
)

dhcp = DHCPServer(
    interface="wlan0",
    ip_range="192.168.100.10-192.168.100.100",
    gateway="192.168.100.1",
    dns_servers=["8.8.8.8", "1.1.1.1"]
)

hotspot = Hotspot(
    ssid="Enterprise-WiFi",
    interface="wlan0",
    security=security,
    dhcp_server=dhcp,
    channel=6,
    hidden=False
)

# Monitor hotspot status
if hotspot.start():
    while hotspot.is_running():
        devices = hotspot.get_connected_devices()
        print(f"Active connections: {len(devices)}")

        for device in devices:
            print(f"  {device['mac']} -> {device['ip']} ({device['hostname']})")

        time.sleep(30)  # Update every 30 seconds
```

---

## 📡 Hotspot Management

Gatenet provides **enterprise-grade Wi-Fi access point management** with cross-platform support:

### ✨ **Key Features**

- **🔒 Multiple Security Types:** WPA3, WPA2, WEP, and Open networks
- **🌍 Cross-Platform:** Native Linux (hostapd) and macOS (Internet Sharing) support
- **🔧 DHCP Integration:** Automatic IP assignment with custom ranges and DNS
- **📊 Real-Time Monitoring:** Live device tracking and connection statistics
- **🔑 Password Management:** Secure generation with complexity validation
- **⚙️ Advanced Configuration:** Channel selection, broadcast control, bandwidth limits

### 🚀 **Quick Setup**

```python
from gatenet.hotspot import Hotspot

# Minimal setup - auto-configured for your platform
hotspot = Hotspot(ssid="MyNetwork", password="SecurePass123!")
hotspot.start()
```

---

## 🔍 Service Discovery

**Intelligent service identification** using multiple detection strategies:

### 🎯 **Detection Methods**

- **Banner Analysis:** Deep packet inspection of service banners
- **Port Mapping:** Well-known port to service correlation
- **Keyword Detection:** Flexible pattern matching
- **Custom Detectors:** Extensible plugin architecture

### 🛠️ **Supported Services**

| Protocol     | Services                   | Detection Method   |
| ------------ | -------------------------- | ------------------ |
| **SSH**      | OpenSSH, Dropbear, PuTTY   | Banner parsing     |
| **HTTP**     | Apache, Nginx, IIS, Tomcat | Server headers     |
| **FTP**      | vsftpd, ProFTPD, FileZilla | Welcome messages   |
| **Email**    | Postfix, Exchange, Dovecot | SMTP/IMAP banners  |
| **Database** | MySQL, PostgreSQL, MongoDB | Connection strings |
| **Custom**   | Your services              | Plugin detectors   |

### 🔧 **Custom Detector Example**

```python
from gatenet.service_detectors import ServiceDetector

class DockerDetector(ServiceDetector):
    """Detect Docker daemon on port 2376."""

    def detect(self, port: int, banner: str) -> str:
        if port == 2376 and "docker" in banner.lower():
            return "Docker Daemon"
        return None

# Register and use
discovery = ServiceDiscovery()
discovery.add_detector(DockerDetector())
```

---

## 🧪 Testing & Development

### 🎯 **Comprehensive Test Suite**

```bash
# Run all tests
pytest

# Test specific modules
pytest src/tests/hotspot/
pytest src/tests/diagnostics/

# Generate coverage report
pytest --cov=gatenet --cov-report=html
```

### 🛠️ **Development Tools**

```bash
# Install development dependencies
pip install -e ".[dev]"

# Code formatting
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Documentation
make -C docs html
```

### **Interactive Development**

- **[Try in Browser](https://gatenet.readthedocs.io/en/latest/sandbox.html)** - No installation required
- **Web Dashboard** - Visual interface for all tools
- **CLI Interface** - Command-line access to all features

---

## 📚 Resources

- **[📊 API Reference](https://gatenet.readthedocs.io/en/latest/gatenet.html)**
- **[🔄 Changelog](https://gatenet.readthedocs.io/en/latest/changelog.html)**
- **[📜 Code of Conduct](.github/CODE_OF_CONDUCT.md)**
- **[🤝 Contributing](.github/CONTRIBUTING.md)**
- **[🛡️ Security](.github/SECURITY.md)**
- **[📄 License](LICENSE)**

---

<div align="center">

**Built with ❤️ for the networking community**

[![Documentation](https://img.shields.io/badge/docs-latest-blue?style=for-the-badge)](https://gatenet.readthedocs.io/) [![License](https://img.shields.io/github/license/clxrityy/gatenet?style=for-the-badge)](LICENSE)

[![Coverage](https://img.shields.io/badge/coverage-Report-green?logo=readthedocs&logoColor=%238CA1AF&color=%2333CC99&style=for-the-badge)](https://gatenet.readthedocs.io/en/latest/coverage_summary.html)

</div>
