# gatenet

[![PyPI](https://img.shields.io/pypi/v/gatenet?style=for-the-badge)](https://pypi.org/project/gatenet/)
[![Docs](https://img.shields.io/badge/docs-latest-blue?style=for-the-badge)](https://gatenet.readthedocs.io/en/latest/)
[![CI](https://github.com/clxrityy/gatenet/actions/workflows/test.yml/badge.svg?style=for-the-badge)](https://github.com/clxrityy/gatenet/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/badge/changelog-blueviolet?style=for-the-badge)](https://gatenet.readthedocs.io/en/latest/changelog.html)

Gatenet is a Python toolkit for networking: diagnostics (ping, traceroute, DNS, ports), simple HTTP/TCP/UDP building blocks, service discovery, and Wi‑Fi hotspot management. It now includes a lightweight hooks system for easy extensibility.

## Install

```bash
pip install gatenet
```

Python 3.10+ • Linux/macOS/Windows (feature availability varies by platform)

## Highlights

- Diagnostics: ICMP/TCP ping, traceroute, port scan, DNS, IP geolocation
- HTTP/TCP/UDP: minimal server/client utilities
- Discovery: pluggable detectors with a registry
- Hotspot: create/manage Wi‑Fi access points (Linux/macOS)
- Hooks: shared event bus across modules (HTTP, clients, discovery, diagnostics)

## Quick start

HTTP server

```python
from gatenet.http_.server import HTTPServerComponent

server = HTTPServerComponent(host="127.0.0.1", port=8080)

@server.route("/status", method="GET")
def status(_req):
    return {"ok": True}

server.start()
```

HTTP client

```python
from gatenet.http_.client import HTTPClient

client = HTTPClient("http://127.0.0.1:8080")
res = client.get("/status")
print(res["data"])  # {"ok": True}
```

TCP / UDP

```python
from gatenet.client.tcp import TCPClient
from gatenet.client.udp import UDPClient

# TCP
tcp = TCPClient("127.0.0.1", 9000)
tcp.connect()
print(tcp.send("ping"))
tcp.close()

# UDP
udp = UDPClient("127.0.0.1", 9001)
print(udp.send("ping"))
udp.close()
```

Diagnostics

```python
from gatenet.diagnostics import ping
from gatenet.diagnostics.traceroute import traceroute

print(ping("1.1.1.1", count=2))
print(traceroute("example.com"))
```

Discovery

```python
from gatenet.discovery.ssh import _identify_service

print(_identify_service(22, "SSH-2.0-OpenSSH_8.9p1"))
```

Hotspot (platform-dependent)

```python
from gatenet.hotspot import Hotspot

hotspot = Hotspot(ssid="GatenetAP", password="SecurePass123!")
if hotspot.start():
    print("running")
    hotspot.stop()
```

Hooks & events

```python
from gatenet.core import hooks, events

hooks.on(events.HTTP_BEFORE_REQUEST, lambda req: print("HTTP", req.command, req.path))
```

## Learn more

- Docs: https://gatenet.readthedocs.io
- Examples: docs Examples page (HTTP, TCP/UDP, discovery, diagnostics, hooks)
- Changelog: https://gatenet.readthedocs.io/en/latest/changelog.html

## Contributing

Run tests locally:

```bash
pytest -q
```

License: MIT
