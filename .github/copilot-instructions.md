# Gatenet | Copilot Instructions

Gatenet is a Python package for building and working with socket servers and clients, including TCP, UDP, and HTTP protocols. It provides a simple interface for creating servers and clients, handling requests, and managing connections.

## Package Structure
- `src/`: Contains the main code.
    - `gatenet/`: The main package directory.
        - `__init__.py`: Initializes the package.
        - `client/`: Contains the client implementations.
            - `base.py`: Base client class.
            - `tcp.py`: TCP client class.
            - `udp.py`: UDP client class.
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
- `utils/net.py`: Contains network utilities like `get_free_port()` for finding available ports.
---

## Usage patterns

- Prefer method chaining where appropriate (e.g. for fluent APIs).
- Always include docstrings using Google-style or NumPy-style formatting.
- When returning JSON from HTTP routes, return Python `dict` (not serialized JSON).
- When writing tests:
    - Use `pytest` and `assert`, not `unittest`.
    - Use `get_free_port()` from `gatenet.utils.net` to find an available port for testing and avoid port conflicts.
    - Use `time.sleep()` only when needed to wait for the server to start or for asynchronous operations to complete.
    - Use `pytest.mark.asyncio` for testing asynchronous code.

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

