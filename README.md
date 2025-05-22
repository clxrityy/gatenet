# gatenet 🛰️

##### BETA (0.1.2)

![Changelog](https://img.shields.io/badge/changelog-log?logo=gitbook&logoColor=%23333333&color=%23BBDDE5&link=https%3A%2F%2Fgithub.com%2Fclxrityy%2Fgatenet%2Fblob%2Fmaster%2FCHANGELOG.md)

| | |
|---|---|
| **Package** | [![PyPI](https://img.shields.io/pypi/v/gatenet)](https://pypi.org/project/gatenet/) |
| **Python** | [![Python](https://img.shields.io/pypi/pyversions/gatenet)](https://pypi.org/project/gatenet/) |
| **Tests** | [![CI](https://github.com/clxrityy/gatenet/actions/workflows/test.yml/badge.svg)](https://github.com/clxrityy/gatenet/actions/workflows/test.yml) [![codecov](https://codecov.io/gh/clxrityy/gatenet/graph/badge.svg?token=4644O5NGW9)](https://codecov.io/gh/clxrityy/gatenet) |
| **License** | [![License](https://img.shields.io/github/license/clxrityy/gatenet)](LICENSE) |

> Python networking toolkit for sockets, UDP, and HTTP microservices — modular and testable.

- [Changelog](https://github.com/clxrityy/gatenet/blob/master/CHANGELOG.md)
- [Installation](#installation)
- [Features](#features)
- [TCP](#tcp-server)
- [UDP](#udp-server--client)
- [HTTP](#http-server--client)
- [Tests](#tests)

---

## Installation

```zsh
pip install gatenet
```

## Features
- [x] [TCP](#tcp-server) for raw socket data
- [x] [UDP](#udp-server--client)
- [x] [HTTP](#http-server)
    - [x] Route-based handling
    - [x] JSON responses
    - [x] Dynamic request handling
    - [x] Custom headers
    - [x] Error handling
    - [x] Timeout handling
- Minimal, composable, Pythonic design

## TCP Server

```python
from gatenet.socket.tcp import TCPServer

server = TCPServer(host='127.0.0.1', port=8000)

@server.on_receive
def handle_data(data, addr):
    print(f"[TCP] {addr} sent: {data}")
    return f"Echo: {data}"

server.start()
```

## UDP Server & Client

### UDP Server

```python
from gatenet.socket.udp import UDPServer

server = UDPServer(host="127.0.0.1", port=9000)

@server.on_receive
def handle_udp(data, addr):
    print(f"[UDP] {addr} sent: {data}")
    return f"Got your message: {data}"

server.start()
```

### UDP Client

```python
from gatenet.socket.udp import UDPClient

client = UDPClient(host="127.0.0.1", port=9000)
response = client.send("Hello, UDP!")
print(response)
```

## HTTP Server & Client

### HTTP Server

```python
from gatenet.http.server import HTTPServerComponent

server = HTTPServerComponent(host="127.0.0.1", port=8080)

@server.route("/status", method="GET")
def status(_req):
    return {
        "ok": True
    }

@server.route("/echo", method="POST")
def echo(_req, data):
    return {
        "received": data
    }

server.start()
```

### HTTP Client

```python
from gatenet.http.client import HTTPClient

client = HTTPClient("http://127.0.0.1:8080")
print(client.get("/status")) # {"ok": True}
print(client.post("/echo", {"x": 1})) # {"received": {"x": 1}}
```


## Tests

```bash
pytest
```