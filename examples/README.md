# GATENET — EXAMPLES

```zsh
pip install gatenet
```

- **HTTP**
  - [GET & POST requests](./http_/http_example.py)
  - [Timeout & retry](./http_/timeout_retry.py)
  - [Asynchronous Client](./http_/async_client_usage.py)
- **TCP & UDP**
  - [With polymorphism](./tcp_udp/polymorphism.py)
- **Diagnostics**
  - [DNS Lookup](./diagnostics/dns_lookup.py)
  - [Port Scanning](./diagnostics/port_scanning.py)
  - [Geo Information](./diagnostics/geo_info.py)
  - [Traceroute](./diagnostics/traceroute.py)
  - [Bandwidth](./diagnostics/bandwidth.py)
  - [Ping](./diagnostics/ping.py)
- **Discovery**
  - [mDNS Discovery](./discovery/mdns_discovery.py) & [SSDP Discovery](./discovery/ssdp_discovery.py)
    - [Dashboard Example](./discovery/dashboard)
  - [Bluetooth Discovery](./discovery/bluetooth_discovery.py) (Synchronous & Asynchronous)
  - [SSH Discovery](./discovery/ssh_discovery.py)
    - Basic service identification
    - Individual detector examples
    - Full discovery with multiple detectors
    - Practical example with multiple detectors
    - Case-sensitve demo
    - Custom detector example
    - Async usage example
