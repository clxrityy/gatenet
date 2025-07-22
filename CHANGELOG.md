# GATENET — CHANGELOG

## OUTLINE

- [v0](#v0) (BETA)
  - [0.1.0](#010)
    - [0.1.1](#011)
  - [0.3.0](#030)
    - [0.3.2](#032)
  - [0.4.0](#040)
  - [0.5.0](#050)
  - [0.7.5](#075)
  - [0.8.0](#080)

# v0 (BETA)

- Project initialization
  - Created the initial project structure and added basic files.
  - Added `pyproject.toml` for package management.
  - Set up `hatchling` for building and publishing the package. ([cd8bb2f](https://github.com/clxrityy/gatenet/commit/cd8bb2ff17d78c00c1a37872b99f8c17b3333e44))

## 0.1.0

- Added `pytest` for testing.
  - Initialized `pytest.ini` for configuration. ([450fe47](https://github.com/clxrityy/gatenet/commit/450fe471ae9b0115fc96a1a6a8ccf243d56f5282))
  - Created `src/tests/` directory for test files.
- Initialized base socket server. ([2af7050](https://github.com/clxrityy/gatenet/commit/2af7050904438c8dcb715e7a09b4c8e8f07eee7a))
- Created **TCP** & **UDP** socket server classes. ([cf31b71](https://github.com/clxrityy/gatenet/commit/cf31b71aa8d99666536adda58b6108f78d0a14b9))
- Added tests for TCP & UDP socket servers.
  - `test_tcp_server.py` for TCP server tests. ([ce5ac65](https://github.com/clxrityy/gatenet/commit/ce5ac6501f4ff481513c447ee701fb23adf0c51f))
  - `test_udp_server.py` for UDP server tests. ([be1ffc6](https://github.com/clxrityy/gatenet/commit/be1ffc60d745bf64cdd1b453e0c31a0001f07521))
- Created **TCP** & **UDP** client classes. ([5ff8a8d](https://github.com/clxrityy/gatenet/commit/5ff8a8dc05bb47d0204659d9279f2b818443e26d))
- Added tests for TCP/UDP client & server. ([2cc6cb5](https://github.com/clxrityy/gatenet/commit/2cc6cb5c3a08cc94d1c380599f1dcfefa3b7f653))
- Added **HTTP** server classes & tests. ([d1ed9df](https://github.com/clxrityy/gatenet/commit/d1ed9dfa82d8edc192fb7cfdabef4d5659169fd7))
- Added **HTTP** client class. ([812683b](https://github.com/clxrityy/gatenet/commit/812683bc93398ea9abba1c7ebd57a910e654cd45))
- Added test for HTTP client. ([a352b48](https://github.com/clxrityy/gatenet/commit/a352b489106b00ccdfcf8901049be8a4af179df8))

## 0.1.1

- Added code coverage support with `codecov`.

## 0.3.0

- Built this changelog. 😏
- Added **Dynamic Request Handling** for HTTP server. ([bf8658c](https://github.com/clxrityy/gatenet/commit/bf8658cb78f02cf7fdd2a0a0583f568eb99eb8e0))
  - Centralized `_handle()` method inside the generated `RouteHTTPRequestHandler`
  - Support for all standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`).
  - Automatically deserializes JSON from `POST`, `PUT`, `PATCH` etc., and returns responses with `200`, `404` or `500` status codes.
  - Dispatched dynamically using one route registry.
- Improved `HTTPClient` ([f02ae1a](https://github.com/clxrityy/gatenet/commit/f02ae1a5c0c0c74ba54cc5e95220f699fb2baf6c))
  - Handles:
    - Custom headers
    - Timeouts
    - HTTP & URL errors
  - Default JSON headers are applied if none are provided.
  - Error responses are parsed into structured dicts like:
    ```json
    {
      "error": "Not Found",
      "code": 404
    }
    ```
- Test cases for HTTP server/client updated. ([ef735bd](https://github.com/clxrityy/gatenet/commit/ef735bd60e86da12c812d38f969e325feefa0973)) & ([a2f896e](https://github.com/clxrityy/gatenet/commit/a2f896ef14121294c1f6d3b48821ca0c4394860e))

  - Uses only the `@route` decorators for route registration.
  - Verifies proper roundtrip of JSON data with `POST`.
  - Verifies status routes, echo routes, and default error handling.

- Refactored the `HTTPClient` class to manage all HTTP methods (GET, POST, PUT, DELETE, PATCH) in a single method. ([2e4d986](https://github.com/clxrityy/gatenet/commit/2e4d98615c5ab3dce8986966bd00a891bad56746))
  ```python
  for m in ["get", "post", "put", "delete", "patch"]:
      setattr(
          #...
      )
  ```
  - Add a wrapper method with docstrings and type hints.
    ```python
    def _generate_method(self, method: str):
        def _method(
            # ... arguments
        )
            return self._request(
                # ... arguments
            )
        _method.__name__ = method
        _method.__doc__ = f"Send an HTTP {method.upper()} request"
    return _method
    ```
  - Add support for custom headers, timeouts, and error handling.
- Added some [examples](./examples/README.md) ([cce8f2d](https://github.com/clxrityy/gatenet/commit/cce8f2d3f94e2c8a33e5417203ef87d8c29060c6))

## 0.3.2

- Added `BaseClient` class for TCP & UDP clients. ([e3bd9a3](https://github.com/clxrityy/gatenet/commit/e3bd9a3216dfd73f721cf50b90dc0eac1c82663a))
- **TCP** & **UDP** clients now inherit from `BaseClient`. ([48bcb70](https://github.com/clxrityy/gatenet/commit/48bcb709b04b40f006c9cc91b9a27cdc13b8b490))
  - Both classes now support a `timeout` parameter.
  - Both classes now support a `buffsize` parameter within `send()`
    - **UDP** client also accepts a `retries` parameter (3 by default).
- Added `AsyncHTTPClient` class for asynchronous HTTP requests. ([7bfff14](https://github.com/clxrityy/gatenet/commit/7bfff14d62edaf2061a551aad042087920406929))
  - Uses `aiohttp` for asynchronous HTTP requests.
  - Supports GET & POST methods.
  - Also added corresponding test & example files.
- Added a polymorphic example for TCP & UDP clients. ([3bcff36](https://github.com/clxrityy/gatenet/commit/3bcff36e932c57afd997b19175b8b4ffa2133c73))
- Freezed all requirements into `requirements.txt` ([45d860d](https://github.com/clxrityy/gatenet/commit/45d860d1c48f77fe868a023e44b1d8bdd685e761))
- Added `.github/copilot-instructions.md` for GitHub Copilot instructions. ([e1fdb83](https://github.com/clxrityy/gatenet/commit/e1fdb83882cf4bad6186892b94458b95b17b7d08))

## 0.4.0

> The diagnostics module has been added in this version, which includes various network diagnostics and test suites.

- Added `gatenet.diagnostics` module for network diagnostics & test suites. ([0ce9629](https://github.com/clxrityy/gatenet/commit/0ce9629c3ebbff2b3bb918fbcb256dd1892175e3)), includes:
  - **DNS**:
    - `reverse_dns_lookup()` - DNS lookup for a given IP address.
    - `dns_lookup()` - DNS lookup for a given domain name.
  - **Ports**:
    - `check_public_port()` - Check if a TCP port is publicly accessible. (Defaults to host `1.1.1.1` (Cloudflare DNS), and port `53` (DNS port))
    - `scan_ports()` - Scan a list of ports on a given host, defaults to common ports.
    - `check_port()` (**ASYNC**) - Utilizes `asyncio` to check if a port is open on a given host.
    - `scan_ports_async()` (**ASYNC**) - Utilizes `asyncio` to scan a list of ports (defaults to common ports) on a given host.
  - **Geo**:
    - `get_geo_info()` - Get geographical information for a given IP address.
- Also added `ping()` function to `gatenet.diagnostics` module for pinging a host. ([7fa243ea](https://github.com/clxrityy/gatenet/commit/7fa243ea1517d0c29b10d328725f3514a998c401))
  - Uses `subprocess` to execute the `ping` command.
  - Added tests.
- Restructured the package to be more modular and organized. ([b3edf059](https://github.com/clxrityy/gatenet/commit/b3edf059482ac1b32e458339c2469e2fb0e175aa)).

  - Added `__init__.py` files to each module.

  ```py
  # import before
  from gatenet.http.server import HTTPServerComoonent

  # import after
  from gatenet.http import HTTPServerComponent
  ```

- Added [examples](https://github.com/clxrityy/gatenet/tree/master/examples/diagnostics) for the new diagnostics module. ([938514f](https://github.com/clxrityy/gatenet/commit/938514f8e8bf7a1edf1ea597c92187e9c7ab4f96))

## 0.5.0

- Added `async_ping` to `gatenet.diagnostics` module for asynchronous pinging of a host. ([a552753](https://github.com/clxrityy/gatenet/commit/a552753f445bc80e35086be9bdc3854b78e22fcc))
- Added docs

## 0.7.5

- Added `gatenet.discovery` module for service discoveries. ([7f43e31](https://github.com/clxrityy/gatenet/commit/7f43e31dea614b11c5e2dfe837b5285b3a65b8ee))
  - Added support for mDNS service discovery.
    - **`gatenet.discovery.mdns`** module for mDNS service discovery.
    - `MDNSListener` class for listening to mDNS events.
    - `discover_mdns_services()` function for discovering mDNS services.
    - Added a test for mDNS service discovery.
    - `add_service()` method to `MDNSListener` for adding discovered services.
  - Added support for SSDP (UPnP) service discovery.
    - **`gatenet.discovery.upnp`** module for SSDP service discovery.
    - `discover_upnp_devices()` function for discovering UPnP devices.
    - Added a test for SSDP service discovery.
  - Added examples for mDNS and SSDP service discovery.
    - `examples/discovery/mdns_example.py` for mDNS & `examples/discovery/upnp_example.py` for SSDP service discovery example. ([da73cf86](https://github.com/clxrityy/gatenet/commit/da73cf86f89354cdfebfb3a40f908120d9418867))
    - Added `examples/discovery/dashboard` for a simple dashboard to display discovered services. ([f256dfb](https://github.com/clxrityy/gatenet/commit/f256dfb53687631bb050003f485974624daecb95))
  - Added `gatenet.discovery.bluetooth` module for Bluetooth service discovery (Synchronous and Asynchronous) with corresponding tests and examples. ([ce15ec7](https://github.com/clxrityy/gatenet/commit/ce15ec7d46e7456e97d48a19a4dfcd6e54237faf))
  - Added `gatenet.discovery.ssh` module for SSH service discovery. ([7cb84be0](https://github.com/clxrityy/gatenet/commit/7cb84be0ac2c6c8928d79fafff95cf821550984b))
    - `SSHDetector` class for detecting SSH services.
    - `HTTPDetector`, `FTPDetector`, `SMTPDetector`, `PortMappingDetector`, `BannerKeywordDetector`, and `GenericServiceDetector` classes for detecting various services over SSH.
    - Added tests for SSH service discovery.
    - Added examples for SSH service discovery.
- Added **`traceroute()`** to `gatenet.diagnostics`. ([009e906](https://github.com/clxrityy/gatenet/commit/009e9060c8f506bb5f3fad53ba292dd3149cd457))
  - Added corresponding example & test(s).
- Added [CONTRIBUTING](https://github.com/clxrityy/gatenet/blob/master/CONTRIBUTING.md) and [CODE_OF_CONDUCT](https://github.com/clxrityy/gatenet/blob/master/CODE_OF_CONDUCT.md) files. ([9b56d5c](https://github.com/clxrityy/gatenet/commit/9b56d5ce9e601f566df4cb1cc38a9a183c126c3c))

## 0.8.0

Diagnostics module improvements and new features.

- Added `gatenet.diagnostics.bandwidth` module for bandwidth measurement. ([16d477dd](https://github.com/clxrityy/gatenet/commit/16d477dd22ababa99c7a71c1bece0bfb75308970))
  - Added examples for download and upload measurement.
  - Added tests.
- Made `gatenet.diagnostics.traceroute` module more robust and user-friendly. ([513524ab](https://github.com/clxrityy/gatenet/commit/513524ab145244e762190bb704fdeaef690d9215))
  > - Supports both UDP and ICMP protocols (choose with the protocol argument).
  > - Returns a list of dicts with hop, IP, hostname, and RTT.
  > - Optionally prints output (print_output argument).
  > - Improved docstring with a clear usage example.
  > - Handles permission errors and host resolution gracefully.
- `gatenet.diagnostics.ping` module improvements. ([0f165d8](https://github.com/clxrityy/gatenet/commit/0f165d8d16ddda822c7119c4ae916459cb66df95))
  - Jitter calculatuon & RTT list:
    - Both sync and async ping now return all individual RTTs and compute jitter.
  - TCP ping support:
    - Added TCP-based ping as a fallback or alternative to ICMP ping.
  - Async improvements:
    - Functions use per-ping and total-operation timeout context managers for robust timeout handling.
    - Async TCP ping uses `asyncio` for non-blocking operations.
  - Refactoring for readability and maintainability:
    - Split into smaller functions for better organization.
    - Improved error handling and logging.
  - Cleaner API:
    - The async helpers no longer take a timeout argument, as they use context managers.
    - Ping functions return a structed results dict:
      - min/avg/max/jitter
      - all RTTs
      - packet loss
      - error info
      - raw output
  - Improved docstrings:
    - Added/updated all and usage examples.
  - Improved error and timeout handling.
- `gatenet.diagnostics.geo` module improvements. ([e533c43](https://github.com/clxrityy/gatenet/commit/e533c43cd95080bdbf302eb2efc2a48dd8177bb7))
  - Improved error handling and consistent return structure for geo lookups.
  - Added Google-style docstrings and clarified API.
  - Now always returns a dict with error info on failure.
  - Example return and error cases documented in the function docstring.
- `gatenet.diagnostics.port_scan` module improvements. ([f1a9deaf](https://github.com/clxrityy/gatenet/commit/f1a9deaf6a3fc19dfad170c9915d4b1957f88a0a))
  - Improved error handling and consistent return structure for all port scan functions.
  - Added Google-style docstrings and clarified API for all sync and async functions.
  - Async port scan helpers now use timeout context managers for robust timeout handling (no timeout argument).
  - Handles edge cases and exceptions more gracefully.
- Fixed and revamped all tests. ([d2a90a83](https://github.com/clxrityy/gatenet/commit/d2a90a83adeb662eeda99c13ff53f9f2827bf1fd))

## 0.8.2

Docstring improvements.

- Updated README.
- Updated `gatenet.client` modules with improved docstrings. ([153eb59a](https://github.com/clxrityy/gatenet/commit/153eb59a7550f6e56790d1e093ce8d6893c80d9e))
- Updated `gatenet.socket` modules with improved docstrings. ([671e4fd1](https://github.com/clxrityy/gatenet/commit/671e4fd17a20fd0d0d31dbdc0c752a139521a9f0))
- Updated `gatenet.http_` modules with improved docstrings. ([a77ce983](https://github.com/clxrityy/gatenet/commit/a77ce98383eb448f12072f17a4ca44ff2b3e9790))
- Updated `gatenet.discovery` modules with improved docstrings. ([d1c84f19](https://github.com/clxrityy/gatenet/commit/d1c84f198bedac97add12a660a745c0b497bbc5b))
- Updated `gatenet.utils` modules with improved docstrings. ([3d3a63a7](https://github.com/clxrityy/gatenet/commit/3d3a63a7e4676430f2aceabf8b2cfb3c8a65f405))
