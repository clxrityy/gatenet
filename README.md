# gatenet 🛰️

##### BETA (0.1.0)

[![CI](https://github.com/clxrityy/gatenet/actions/workflows/test.yml/badge.svg)](https://github.com/clxrityy/gatenet/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/clxrityy/gatenet/graph/badge.svg?token=4644O5NGW9)](https://codecov.io/gh/clxrityy/gatenet)
[![PyPI version](https://img.shields.io/pypi/v/gatenet)](https://pypi.org/project/gatenet/)
[![Python](https://img.shields.io/pypi/pyversions/gatenet)](https://pypi.org/project/gatenet/)
[![License](https://img.shields.io/github/license/clxrityy/gatenet)](LICENSE)

> Python networking toolkit for sockets, UDP, and HTTP microservices — modular and testable.

## Installation

```zsh
pip install gatenet
```

## Features
- [x] [TCP Server](#tcp-server) for raw socket data
- [x] [UDP Server & Client](#udp-server--client)
- [x] [HTTP Server](#http-server)
    - [x] Route-based handling
    - [x] JSON responses
    - [x] POST support
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
from gatenet.http.base import HTTPServerComponent

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