# Gatenet | Copilot Instructions

Gatenet is a modular Python networking toolkit for diagnostics, service discovery, and robust socket/HTTP microservices. It is designed for extensibility, testability, and modern async support.

---

## Package Structure & Directory Layout

- `src/gatenet/` — Main package code
  - `client/` — TCP, UDP, and HTTP clients (sync and async)
  - `socket/` — TCP and UDP socket servers (low-level, connection-oriented)
  - `http_/` — HTTP server and client (sync and async, built on `http.server`, `urllib`, and `aiohttp`)
  - `diagnostics/` — Tools for ping, traceroute, bandwidth, geo IP, DNS, port scanning
  - `discovery/` — Service discovery using strategy and chain-of-responsibility patterns (SSH, HTTP, FTP, SMTP, mDNS, Bluetooth, UPNP, etc.)
  - `utils/` — Utilities (e.g., `get_free_port()`)
- `src/tests/` — Unit and integration tests, mirroring the main package structure
- `examples/` — Example scripts for diagnostics, discovery, HTTP, TCP/UDP, and dashboard usage
- `docs/` — Sphinx documentation, with automated coverage summary
- `Makefile` — Automation for testing, coverage, docs, and release

---

## Design Patterns & Extensibility

- **Strategy Pattern**: Used for service detectors (e.g., SSH, HTTP, FTP, SMTP)
- **Chain of Responsibility**: Service identification tries detectors in sequence until one succeeds
- **Abstract Base Classes (ABC)**: For extensible interfaces (clients, servers, detectors)
- **Async/Await**: Async support for HTTP, ping, and more
- **Method Chaining**: Fluent APIs for HTTP clients and other components

---

## Usage Patterns & Best Practices

- Prefer method chaining for fluent APIs (e.g., HTTPClient)
- Always include docstrings using Google-style or NumPy-style formatting
- Use type hints for all public functions and classes
- When returning JSON from HTTP routes, return a Python `dict` (not serialized JSON)
- Use ABCs for extensible interfaces (see `BaseClient`, `BaseSocketServer`, `ServiceDetector`)
- Use strategy and chain-of-responsibility for extensible functionality (as in service discovery)
- Prefer async/await for new async features (see `AsyncHTTPClient`, `async_ping`)

---

## Example Usages

**TCP Client (sync and async):**

```python
# Synchronous
from gatenet.client.tcp import TCPClient
client = TCPClient(host="127.0.0.1", port=12345)
client.connect()
response = client.send("ping")
client.close()

# Async
from gatenet.client.tcp import AsyncTCPClient
import asyncio
async def main():
    client = AsyncTCPClient(host="127.0.0.1", port=12345)
    await client.connect()
    response = await client.send("ping")
    await client.close()
asyncio.run(main())
```

**HTTP Server (sync and async):**

```python
# Synchronous
from gatenet.http_.server import HTTPServerComponent
server = HTTPServerComponent(host="0.0.0.0", port=8080)
@server.route("/status", method="GET")
def status_handler(req):
    return {"ok": True}
server.start()

# Async client
from gatenet.http_.async_client import AsyncHTTPClient
import asyncio
async def main():
    client = AsyncHTTPClient("http://localhost:8080")
    response = await client.get("/status")
    print(response)
asyncio.run(main())
```

**Service Discovery:**

```python
from gatenet.discovery.ssh import _identify_service, SSHDetector
service = _identify_service(22, "SSH-2.0-OpenSSH_8.9p1")
print(service)  # Output: "OpenSSH 8.9p1"
ssh_detector = SSHDetector()
result = ssh_detector.detect(22, "ssh-2.0-openssh_8.9p1")
```

**Custom Service Detector:**

```python
from gatenet.discovery.ssh import ServiceDetector
from typing import Optional
class CustomDetector(ServiceDetector):
    def detect(self, port: int, banner: str) -> Optional[str]:
        if 'myapp' in banner:
            return "MyCustomApp"
        return None
```

**Diagnostics (ping, traceroute, bandwidth, geo, DNS, port scan):**

```python
from gatenet.diagnostics.ping import ping, async_ping
result = ping("1.1.1.1", count=3)
import asyncio
asyncio.run(async_ping("8.8.8.8", count=3))

from gatenet.diagnostics.traceroute import traceroute
hops = traceroute("google.com")

from gatenet.diagnostics.bandwidth import measure_bandwidth
result = measure_bandwidth("google.com")

from gatenet.diagnostics.geo import get_geo_info
geo = get_geo_info("8.8.8.8")

from gatenet.diagnostics.dns import dns_lookup, reverse_dns_lookup
ip = dns_lookup("google.com")
host = reverse_dns_lookup("8.8.8.8")

from gatenet.diagnostics.port_scan import scan_ports, check_public_port
open_ports = scan_ports("127.0.0.1", ports=[22, 80, 443])
is_open = check_public_port("1.1.1.1", 53)
```

---

## Testing Guidelines

- Use `pytest` and `assert` for all tests
- Place tests in the appropriate subdirectory under `src/tests/`
- Use `get_free_port()` from `gatenet.utils.net` to avoid port conflicts in tests
- Use `pytest.mark.asyncio` for async tests
- Mock network connections with `unittest.mock` or `pytest` fixtures
- Test both positive and negative cases, including edge cases (timeouts, empty responses, case sensitivity)
- Run `make test` before submitting a PR

---

## Coverage & Documentation

- Coverage is measured with `pytest-cov` and summarized in the docs (see `make docs`)
- Sphinx docs are in `docs/` and built with `make docs`
- Examples are in `examples/` and should be kept up to date with new features

---

## General Best Practices

- Keep code modular and extensible
- Use ABCs and patterns for extensibility
- Prefer async/await for new async features
- Always document public APIs and provide usage examples
- Keep tests and examples up to date with new features

---

## Usage patterns

- Prefer method chaining where appropriate (e.g. for fluent APIs).
- Always include docstrings using Google-style or NumPy-style formatting.
- When returning JSON from HTTP routes, return Python `dict` (not serialized JSON).
- Use strategy pattern and chain of responsibility for extensible functionality (as seen in service discovery).
- Implement abstract base classes (ABC) for defining interfaces that concrete classes must implement.
- When writing tests:
  - Use `pytest` and `assert`, not `unittest`.
  - Use `get_free_port()` from `gatenet.utils.net` to find an available port for testing and avoid port conflicts.
  - Use `time.sleep()` only when needed to wait for the server to start or for asynchronous operations to complete.
  - Use `pytest.mark.asyncio` for testing asynchronous code.
  - Test both individual components and integration scenarios.
  - Include edge case testing (timeouts, empty responses, case sensitivity).

### Example usages

Example GET route:

```python
@server.route("/status", method="GET")
def status_handler(req):
    return {
        "ok": True
    }
```

Example TCP client use:

```python
client = TCPClient(host="127.0.0.1", port=12345)
client.connect()
response = client.send("ping")
client.close()
```

Example service discovery:

```python
from gatenet.discovery.ssh import _identify_service

# Identify service from port and banner
service = _identify_service(22, "SSH-2.0-OpenSSH_8.9p1")
print(service)  # Output: "OpenSSH 8.9p1"

# Use individual detectors
from gatenet.discovery.ssh import SSHDetector
ssh_detector = SSHDetector()
result = ssh_detector.detect(22, "ssh-2.0-openssh_8.9p1")
```

Example custom service detector:

```python
from gatenet.discovery.ssh import ServiceDetector
from typing import Optional

class CustomDetector(ServiceDetector):
    """Custom service detector implementation."""

    def detect(self, port: int, banner: str) -> Optional[str]:
        if 'myapp' in banner:
            return "MyCustomApp"
        return None
```

### Design Patterns Used

- **Strategy Pattern**: Service detectors implement a common interface but provide different detection algorithms.
- **Chain of Responsibility**: Service identification tries detectors in sequence until one succeeds.
- **Abstract Base Classes**: Define interfaces that concrete implementations must follow.
- **Async/Await**: Support for asynchronous operations in network communication.

### Testing Guidelines

- Mock network connections using `unittest.mock` for reliable tests.
- Use `AsyncMock` for testing asynchronous functions.
- Test both positive and negative cases for each detector.
- Verify that fallback mechanisms work correctly.
- Test case insensitivity and whitespace handling.
- Ensure chain of responsibility stops at first match.
