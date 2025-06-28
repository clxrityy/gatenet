# Gatenet | Copilot Instructions

Gatenet is a Python package for building and working with socket servers and clients, including TCP, UDP, and HTTP protocols. It provides a simple interface for creating servers and clients, handling requests, managing connections, and discovering network services.

## Package Structure

- `src/`: Contains the main code.
  - `gatenet/`: The main package directory.
    - `__init__.py`: Initializes the package.
    - `client/`: Contains the client implementations.
      - `base.py`: Base client class.
      - `tcp.py`: TCP client class.
      - `udp.py`: UDP client class.
    - `discovery/`: Contains network service discovery implementations.
      - `ssh.py`: Service detection using strategy pattern (SSH, HTTP, FTP, SMTP, etc.).
    - `http/`: Contains the HTTP client and server implementations.
      - `base.py`: Contains `SimpleHTTPRequestHandler`
      - `client.py`: HTTP client class.
      - `server.py`: HTTP server component class.
      - `async_client.py`: Asynchronous HTTP client class.
    - `socket/`: Contains the socket server implementations.
      - `base.py`: Base socket server class.
      - `tcp.py`: TCP socket server class.
      - `udp.py`: UDP socket server class.
    - `utils/`: Contains utility functions and classes.
      - `net.py`: Network utilities (`get_free_port()`, ...).
  - `tests/`: Contains the test suite.
    - `client/`: Tests for client classes.
      - `test_tcp_client.py`: Tests for TCP client.
      - `test_udp_client.py`: Tests for UDP client.
    - `discovery/`: Tests for service discovery.
      - `test_ssh_discovery.py`: Tests for service detection functionality.
    - `http/`: Tests for HTTP client and server.
      - `test_http_client.py`: Tests for HTTP client.
      - `test_http_server.py`: Tests for HTTP server.
      - `test_async_client.py`: Tests for asynchronous HTTP client.
    - `socket/`: Tests for socket server classes.
      - `test_tcp_server.py`: Tests for TCP socket server.
      - `test_udp_server.py`: Tests for UDP socket server.
    - `utils/`: Tests for utility functions.
      - `test_net_utils.py`: Tests for network utilities.
- `examples/`: Contains example scripts demonstrating usage.
  - `discovery/`: Service discovery examples.
    - `ssh_discovery.py`: Examples of service detection usage.
- `CHANGELOG.md`: Contains the changelog for the package.
- `README.md`: The main documentation file for the package.
- `pyproject.toml`: Configuration file for the package.
- `pytest.ini`: Configuration file for pytest.
- `requirements.txt`: Contains the package dependencies.
- `LICENSE`: The license file for the package.

### Folder roles

- `client/`: Only contains protocol specific clients (TCP, UDP, HTTP).
- `socket/`: Contains protocol specific socket servers. These are low-level and connection-oriented.
- `http/`: Handles HTTP server and clients - built on top of `http.server` and `urllib` or `aiohttp`.
- `discovery/`: Network service discovery and identification using strategy and chain of responsibility patterns.
- `utils/net.py`: Contains network utilities like `get_free_port()` for finding available ports.

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
