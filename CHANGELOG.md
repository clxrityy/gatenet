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
    - [0.8.2](#082)
    - [0.8.4](#084)
    - [0.8.6](#086)
    - [0.8.8](#088)
    - [0.8.9](#089)
  - [0.9.0](#090)
    - [0.9.5](#095)
    - [0.9.7](#097)
    - [0.9.9](#099)
  - [0.11.0](#0110)
    - [0.11.1](#0111)
    - [0.11.2](#0112)
    - [0.11.3](#0113)
  - [0.12.0](#0120)
    - [0.12.1](#0121)
    - [0.12.3](#0123)
    - [0.12.4](#0124)
    - [0.12.5](#0125)
    - [0.12.6](#0126)

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

### 0.1.1

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
- Added some examples ([cce8f2d](https://github.com/clxrityy/gatenet/commit/cce8f2d3f94e2c8a33e5417203ef87d8c29060c6))

### 0.3.2

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

> New module `gatenet.discovery`.

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

> Diagnostics module improvements and new features.

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

### 0.8.2

> Docstring improvements.

- Updated README.
- Updated `gatenet.client` modules with improved docstrings. ([153eb59a](https://github.com/clxrityy/gatenet/commit/153eb59a7550f6e56790d1e093ce8d6893c80d9e))
- Updated `gatenet.socket` modules with improved docstrings. ([671e4fd1](https://github.com/clxrityy/gatenet/commit/671e4fd17a20fd0d0d31dbdc0c752a139521a9f0))
- Updated `gatenet.http_` modules with improved docstrings. ([a77ce983](https://github.com/clxrityy/gatenet/commit/a77ce98383eb448f12072f17a4ca44ff2b3e9790))
- Updated `gatenet.discovery` modules with improved docstrings. ([d1c84f19](https://github.com/clxrityy/gatenet/commit/d1c84f198bedac97add12a660a745c0b497bbc5b))
- Updated `gatenet.utils` modules with improved docstrings. ([3d3a63a7](https://github.com/clxrityy/gatenet/commit/3d3a63a7e4676430f2aceabf8b2cfb3c8a65f405))

### 0.8.4

> Additions and expansions to tests and examples.

- Added **integration** tests.
  - Created a new test suite for HTTP server/client integration. ([bbf252b](https://github.com/clxrityy/gatenet/commit/bbf252b05e68cc88f9ae96e5a67c0806077bc0bf))
  - Created a new test suite for TCP/UDP server/client integration. ([59b8272](https://github.com/clxrityy/gatenet/commit/59b82725679813f90e5e8e08207b41899474fc08))
  - Altered the `pytest.ini` file to include markers for integration tests and timeouts. ([607dafd](https://github.com/clxrityy/gatenet/commit/607dafd87db0f6b828f4947c464b2dfae4899fce))
  - Added edge case tests for TCP/UDP/HTTP clients and servers. ([0c0556f](https://github.com/clxrityy/gatenet/commit/0c0556fe39da8101c11802896633bbe5aaf5e1e7))
- Added more examples. ([cf7be11](https://github.com/clxrityy/gatenet/commit/cf7be11d8ee8eae7c1c043509be45ede5a59ad9e))

### 0.8.6

> Improve error handling and edge case coverage.

- Fixed security vulnerabilities in `gatenet.socket.base` module. ([f8a6f296](https://github.com/clxrityy/gatenet/commit/f8a6f296e082ec78e2b4001be197a225dc78d65b))
- Added more DNS edge test cases. ([59cc4c2](https://github.com/clxrityy/gatenet/commit/59cc4c2cc5a8fffba48807781b4ea4b5aeae38f7))
- Added a client test for TCP/UDP edge cases. ([9985aa91](https://github.com/clxrityy/gatenet/commit/9985aa91bc59a5ed184c285fd877745a578e6f77))
- Added more tests for the `gatenet.discovery.ssh` module. ([8cc6513](https://github.com/clxrityy/gatenet/commit/8cc6513ca8a05b4d8ef772ca3b4b89d4ae66c027))
  - Tests for ambiguous banners containing multiple service indicators (e.g., both SSH and HTTP, or FTP and HTTP) to ensure the detector chain prioritizes correctly.
- Improved `gatenet.discovery.bluetooth`, `gatenet.discovery.mdns`, and `gatenet.discovery.upnp` modules with better error handling. ([ab9483c](https://github.com/clxrityy/gatenet/commit/ab9483c582fcecf62f366aa0f228393f72bba5fb))
  - All error handling now uses Python's built-in `logging` module instead of `print()`.
  - When an error occurs, the module logs the error message and returns an empty list instead of raising an exception.

### 0.8.8

> Documentation improvements and new features.

- Added more customizations and meta data to the docs. ([75f8dc7](https://github.com/clxrityy/gatenet/commit/75f8dc72e8670e3b353950ad72a9fadd590d0eb2))
  - Footer animation.
- Added various styles and a hero section to the docs. ([911ecb4](https://github.com/clxrityy/gatenet/commit/911ecb416b6f7ab1ca731aac8a0ee9a57ddb90a0))
- Ensured **every** module has proper docstrings and usage examples. ([71e6263](https://github.com/clxrityy/gatenet/commit/71e62638187df7516f973fce5985f46ab91ebade))

### 0.8.9

> Coverage documentation & development automation.

- Added dependencies for coverage reporting and documentation generation. ([ed753462](https://github.com/clxrityy/gatenet/commit/ed753462c32ca136a17cc01967b3cbd85943b967))
- The docs now support and display the code coverage reports.
- Added a **`Makefile`** for easier development automation through common task scripts. ([90d7a12](https://github.com/clxrityy/gatenet/commit/90d7a12de883733053388f57d2456b479156abe8))
  ##### Main commands:
  **`make help`** - Show all available commands.
  **`make venv`** - Create a virtual environment.
  **`make install`** - Install all dependencies.
  **`make test`** - Run all tests.
  **`make coverage`** - Generate a coverage report.
  **`make docs`** - Generate the documentation.
  **`make clean`** - Clean up the project build/dist directories/files.
  **`make build`** - Build the package.
  **`make release`** - Release the package.
  **`make version`** - Display the current version and update the version within `pyproject.toml` & `docs/source/conf.py`.

## 0.9.0

> Documentation SEO improvements and repository maintenance/necessities.

- Updated the vital markdown files:
  - `README.md` - Now includes async examples and a better reflection of the package's capabilities.
  - `CONTRIBUTING.md` - Updated to provide clearer guidelines for contributing to the project.
  - `.github/copilot-instructions.md` - Added instructions for using GitHub Copilot with the project.
- Added a `SECURITY.md` file to outline the security policy and reporting guidelines.
- Added more SEO support to the documentation.
  - A sitemap will be generated automatically (through `sphinx-sitemap`).
  - OpenGraph/meta tags and keywords are configured (through `sphinxext-opengraph`).
  - Added a `robots.txt` file to point to the sitemap.
- Integrated the changelog into the documentation.
  - Installed `myst-parser` to parse the changelog markdown.
  - Added a new section in the documentation to display the changelog.
  ```zsh
  make docs
  ```
- Added more sphinx extensions to slightly enhance the documentation.
  - `sphinx_copybutton` - Adds "Copy" buttons to code blocks.
  - `sphinx_inline_tabs` - Enables inline tabbed content.
  - `sphinx_design` - Adds design elements and utilities.
- Added more `.github/` files for repository maintenance.
  - `ISSUE_TEMPLATE/` - Issue templates for bug reports and feature requests.
    - `bug_report.md` - Template for reporting bugs.
    - `feature_request.md` - Template for requesting new features.
  - `pull_request_template.md` - Template for pull requests.
- Added an **architecture diagram** to the documentation.
  - The diagram is generated using `sphinxcontrib-mermaid`.
  - It provides a visual representation of the package's structure and components using a mind map.

### 0.9.5

> Dashboard module addition & documentation improvements.

- Added examples within the documentation.
- Added `gatenet.dashboard` module for a modern FastAPI-based dashboard.
- Provides a web UI and API endpoints for diagnostics (ping, traceroute, DNS lookup, port scan) and live output (SSE traceroute).
- Usage:

  ```python
  from gatenet.dashboard import launch_dashboard

  # Launch the dashboard (opens browser by default)
  launch_dashboard(host="127.0.0.1", port=8000, open_browser=True)
  # The dashboard will be available at http://127.0.0.1:8000
  ```

- The FastAPI `app` instance is also available for advanced integration:
  ```python
  from gatenet.dashboard.app import app
  ```
- Features:
  - Interactive web UI for diagnostics (ping, traceroute, DNS lookup, port scan)
  - Live traceroute output using Server-Sent Events (SSE)
  - REST API endpoints for all diagnostics
  - CORS enabled for local development
- Test coverage:
  - Added `src/tests/dashboard/test_dashboard_api.py` with pytest-based tests for all dashboard endpoints, including live SSE stream.
- Updated the `gatenet.diagnostics.bandwidth` example to instruct the user to run an appropriate server before testing the bandwidth measurement.
- Updated the documentation navigation and styles.

### 0.9.7

> New service detection capabilities for additional protocols and services.

- Added support for detecting the following protocols and services (`gatenet.service_detectors`):
  - `HTTPDetector` for HTTP services
  - `FTPDetector` for FTP services
  - `SMTPDetector` for SMTP services
  - `IMAPDetector` for IMAP services
  - `POP3Detector` for POP3 services
  - `SIPDetector` for SIP services
  - `MQTTDetector` for MQTT services
  - `CoAPDetector` for CoAP services
  - `BannerKeywordDetector` for detecting services based on specific banner keywords
  - `PortMappingDetector` for mapping ports to services
  - `SSHDetector` for SSH services
- Added `ServiceDiscovery` class (`gatenet.discovery.service_discovery`) for service detection.
- Updated docs:
  - Architecture diagram
  - Hero design
  - Improved API reference

### 0.9.9

- Initialized the `gatenet.cli` module for command-line interface functionality.
  ```zsh
  # Run locally
  python -m gatenet.cli
  # Or install the package and run
  gatenet <command> [options]
  ```
  - Added commands:
    - `iface` - List network interfaces and their details.
    - `wifi` - Scan for available WiFi networks (SSID, signal, security).
    - `ping` - Ping a host or IP address.
    - `trace` - Perform a traceroute to a host.
    - `dns` - Perform DNS lookups and reverse lookups.
    - `ports` - Scan TCP/UDP ports on a host.
- Updated documentation:
  - Added CLI usage examples and command reference.
  - Added CLI architecture diagram.
- Added `gatenet.cli` tests for all commands.

## 0.11.0

##### Major changes

- Added `gatenet.mesh` module for mesh networking capabilities.
  - Provides modular mesh networking with support for LoRa, ESP, Wi-Fi, GPS, and SDR integration.
  - Enables encrypted messaging, packet parsing, and topology mapping across mesh nodes.
  - Supports logging GPS location and RF signal strength, tagging packets and mesh topology.
  - Includes Wi-Fi SSID/device scanning and correlation (Raspberry Pi compatible).
  - Hardware integration guides and CLI examples for mesh, radio, and protocol features.
  - Extensible for new protocols and hardware (e.g., SDR, custom radios).
- Added `gatenet.mesh` tests for all features.
- The documentation now sets the following HTTP security headers for improved security and browser policy enforcement:
  - `Content-Security-Policy`: Restricts sources to self, disables inline scripts, and limits external assets.
  - `X-Frame-Options: SAMEORIGIN`: Prevents clickjacking by disallowing framing from other origins.
  - `Permissions-Policy`: Disables geolocation, microphone, camera, and restricts fullscreen to self.
  - `Access-Control-Allow-Origin: https://gatenet.readthedocs.io`: Restricts cross-origin requests to the official docs domain for secure CORS.

##### Utility changes

- Updated `Makefile` to include a new script for removing empty files (apart from `__init__.py` files).
- Updated the official description.
- Updated the architecture diagram to include the new `gatenet.mesh` module.
- Added a sub-section on the documentation for _Additional Resources_.
  - Includes hardware integration guides, protocol documentation, and CLI examples.
    - Refactored all modules to improve docstrings to include usage examples and/or applicable references.
    - Added more tests:
      - Edge case tests for diagnostics modules:
        - `test_ping_edge.py` and async ping edge cases
        - `test_bandwidth_edge.py` for invalid host, zero duration, negative payload
        - `test_port_scan_edge.py` for invalid hosts, empty port lists
        - `test_dns_edge.py` for invalid domain/IP lookups
        - `test_traceroute_edge.py` for invalid hosts, zero hops
      - ABC and constructor tests:
        - `test_base_socket_server.py` for `BaseSocketServer` ABC
        - `test_base_client.py` for `BaseClient` ABC
      - Repr and boundary tests:
        - `test_tcp_udp_client_repr.py` for TCP/UDP client `__repr__`
        - `test_constants_edge.py` for `COMMON_PORTS` type and nonempty
        - `test_net_edge.py` for `get_free_port` uniqueness and type
      - These tests improve coverage for error handling, edge cases, and abstract base classes across diagnostics, client, socket, and utils modules.
- Updated all meta markdown files for consistency and clarity.
- Added workflows:
  - `release.yml` for automated release upon github release creation.
  - `test-release.yml` for releasing to TestPyPI upon pushing to the `development` branch.

### 0.11.1

- Added `gatenet.radio` module for radio frequency (RF) detection and event-driven mesh integration.
  - Supports SDR, LoRa, and ESP hardware for RF signal propagation.
  - Enables encrypted messaging, diagnostics, and robust topology mapping.
  - Includes `MeshRadio`, `LoRaRadio`, and `ESPRadio` classes for RF event handling and packet tagging.
  - Provides a unified interface for RF detection and mesh networking.
- Improved diagnostics module with:
  - `ping_with_rf` for RF-based pinging.
  - Enhanced host validation and error handling.
  - Removed unreachable code for reliability.
- Fixed method signature mismatches and unreachable code in mesh, radio, and diagnostics modules.
- Updated docstrings and usage examples for mesh, radio, and diagnostics modules to clarify APIs and extensibility.
- Resolved all recent errors and lint issues; added event handler safety checks for mesh/radio integration.
- Validated codebase for compatibility, extensibility, and robust event-driven networking.
- Added standalone `gatenet.radio` module with SDR, LoRa, and ESP classes for RF detection and event-driven mesh integration.
- Mesh and radio modules now support RF signal propagation, encrypted messaging, and diagnostics enhancements.
- MeshRadio, LoRaRadio, ESPRadio classes propagate RF events and support robust topology mapping and packet tagging.
- Diagnostics module improved: added `ping_with_rf`, enhanced host validation, and removed unreachable code for reliability.
- Fixed method signature mismatches and unreachable code in mesh, radio, and diagnostics modules for error-free integration.
- Updated docstrings and usage examples for mesh, radio, and diagnostics modules to clarify APIs and extensibility.
- All recent errors and lint issues resolved; event handler safety checks added to mesh/radio integration.
- CHANGELOG and documentation updated to reflect new architecture, integration points, and expanded test coverage.
- Codebase validated for compatibility, extensibility, and robust event-driven networking.
- Improved security by validating all user inputs and using safe subprocess handling.
- Added radio event examples on the documentation.
- MeshRadio now supports log archival via `sync_logs()`, enabling mesh packet, topology, GPS, RF, and Wi-Fi logs to be saved to a file for base node or Mini PC integration.

### 0.11.2

##### Security improvements

- The ping command is now protected against command injection:
  - It validates the host argument using strict regex for IPv4, IPv6, or valid hostnames before passing to subprocess. This blocks malicious input and follows CodeQL/OWASP recommendations.
- Sensitive exception details are now hidden in the DNS and port scan endpoints.
  - Errors are logged server-side, and users receive a generic message:
    Sensitive exception details are now hidden in the DNS and port scan endpoints.
    > "An internal error occurred. Please try again later."

##### Additional tests

- Added new tests for untested elements in `gatenet.dashboard`:
  - Error handling for invalid host/ports on all endpoints.
  - SSE error path in `/api/traceroute/stream`.
  - CORS headers
  - The `launch_dashboard()` function.
- Additional integration test:
  - MeshRadio GPS, RF, and Wi-Fi logging.
  - Integration with `ping_with_rf`
  - Sending/receiving messages with RF info
  - Topology updates

### 0.11.3

Fixed security vulnerabilities in the ping command.

- Host validation uses a strict allowlist (`_is_valid_host`) before any subprocess call.
- No unchecked user input is ever passed to the command line.
- All shell metacharacters and invalid formats are rejected before execution.

## 0.12.0

Fixed the package imports and CLI.

Created the `gatenet.hotspot` module for comprehensive Wi-Fi access point management.

- **Hotspot Management**: Complete Wi-Fi access point creation and management with cross-platform support for Linux and macOS
  - `Hotspot` class for creating and managing Wi-Fi access points
  - Support for WPA2, WPA3, WEP, and open security configurations
  - Cross-platform compatibility with Linux (hostapd) and macOS (Internet Sharing)
  - Real-time monitoring of connected devices and hotspot status
- **DHCP Server Control**: Integrated DHCP server management for IP address assignment
  - `DHCPServer` class with configurable IP ranges and DNS settings
  - Platform-specific implementations using dnsmasq (Linux) and built-in services (macOS)
  - Automatic network configuration and gateway setup
- **Security Configuration**: Robust security options and password management
  - `SecurityConfig` class with password validation and strength checking
  - Automatic secure password generation with customizable length
  - Support for multiple security types (WPA2, WPA3, WEP, Open)
  - Password complexity validation and common pattern detection
- **Testing Infrastructure**: Comprehensive test suite with CI/CD compatibility
  - 59 unit and integration tests covering all hotspot functionality
  - Subprocess mocking to prevent password prompts in automated workflows
  - Cross-platform test coverage with platform-specific behavior validation
  - Test isolation ensuring hotspot tests don't interfere with other modules

Security improvements and test infrastructure enhancements.

- **Security Hardening**: Fixed command injection vulnerabilities in ping diagnostics
  - Host validation uses a strict allowlist (`_is_valid_host`) before any subprocess call
  - No unchecked user input is ever passed to the command line
  - All shell metacharacters and invalid formats are rejected before execution
- **Dashboard Security**: Improved error handling to prevent information exposure
  - Sanitized exception messages in FastAPI error responses
  - Removed sensitive system information from error outputs
- **Test Infrastructure**: Enhanced testing framework with improved isolation

  - Targeted subprocess mocking for hotspot tests to prevent password prompts
  - Preserved real subprocess calls for diagnostic tests requiring actual network operations
  - Improved CI/CD workflow compatibility with automated testing

Added comprehensive interactive sandbox and theme improvements

- **Interactive Sandbox**: Created a complete browser-based playground for Gatenet features
  - Live code editor with syntax highlighting for Python code examples
  - Interactive HTTP client, TCP/UDP client, and service discovery demonstrations
  - Real-time code execution simulation with formatted output display
  - Quick start playground with pre-configured networking examples
  - Embedded dashboard iframe for full Gatenet web interface experience
- **Theme-Aware Design**: Complete dark/light theme support across all documentation
  - CSS custom properties system for seamless theme switching
  - Theme-aware code editors, output terminals, and interactive elements
  - Consistent styling for all Sphinx admonitions (notes, warnings, tips, etc.)
  - Mobile-responsive design with touch-friendly interfaces
  - Smooth transitions and animations between theme modes
- **Version Banner**: Implemented sticky navigation banner
  - Fixed positioning at top of all documentation pages
  - Direct linking to latest release notes in changelog
  - Professional gradient design matching project branding
  - Cross-platform compatibility and accessibility compliance

Added an interactive sandbox page to the documentation.

### 0.12.1

- **Comprehensive Test Coverage Improvements**: Added extensive test suites to achieve 81% overall code coverage:

  - **CLI Testing**: Fixed all 12 failing CLI tests with proper mocking strategies
    - Updated `test_main.py` to use `patch.dict` for command registry mocking instead of individual function patches
    - Fixed argument name mismatches (`host` vs `target`, `query` vs `hostname`) to match actual CLI implementation
    - Corrected error message assertions and help text validation
    - Added proper module execution tests for `__main__.py` entry point
  - **Client Base Class Testing**: Created comprehensive test suite for abstract `BaseClient` class
    - Added ABC compliance tests ensuring proper abstract method enforcement
    - Fixed regex patterns for TypeError messages (`Can't` vs `Cannot`) across Python versions
    - Added concrete implementation validation and inheritance testing
  - **HTTP Base Handler Testing**: Developed complete test coverage for `SimpleHTTPRequestHandler`
    - Renamed test file from `test_base.py` to `test_http_base.py` to resolve import conflicts
    - Added HTTP request/response testing with mock-based isolation
    - Comprehensive testing of GET methods, response content, and logging functionality
  - **Network Utilities Testing**: Enhanced test coverage for `netinfo` module utilities
    - Added tests for network interface enumeration and Wi-Fi scanning functionality
    - Cross-platform testing for macOS and Linux network discovery methods
    - Comprehensive error handling and edge case validation
  - **Hotspot Module Testing**: Expanded test coverage for Wi-Fi access point management
    - Added comprehensive DHCP server testing with platform-specific implementations
    - Security configuration validation with password strength testing
    - Cross-platform hotspot creation and management verification
  - **Test Infrastructure Improvements**: Enhanced testing framework reliability
    - Resolved Python import conflicts by ensuring unique test file names across modules
    - Improved mocking strategies to prevent real network operations during testing
    - Added proper error message validation with exact regex pattern matching
    - All 330+ tests now passing with robust isolation and comprehensive coverage

- **CLI Hotspot Management**: Added comprehensive hotspot CLI command for Wi-Fi access point management
  - **New `gatenet hotspot` command** with multiple actions:
    - `start` - Create and start Wi-Fi hotspots with customizable security settings
    - `stop` - Stop running hotspots
    - `status` - Check hotspot status and platform information
    - `devices` - List connected devices with IP, MAC, and hostname details
    - `generate-password` - Generate secure passwords with customizable length
  - **Security Configuration**: Support for multiple security types (Open, WPA, WPA2, WPA3)
  - **Comprehensive Options**: Configurable SSID, password, interface, IP range, gateway, channel, and hidden network settings
  - **Multi-format Output**: JSON, table, and plain text output formats for all commands
  - **Cross-platform Support**: Compatible with Linux (hostapd) and macOS (Internet Sharing)
  - **Rich CLI Interface**: Beautiful table output with color-coded status and device information
  - **Complete Test Coverage**: 13 comprehensive tests covering all hotspot functionality and error scenarios
  - **Example Usage**:
    ```bash
    gatenet hotspot start --ssid MyHotspot --password securepass123 --security wpa2
    gatenet hotspot status --output json
    gatenet hotspot devices --output table
    gatenet hotspot generate-password --length 16
    gatenet hotspot stop
    ```
  - All 330 tests now passing with robust isolation and comprehensive coverage

### 0.12.3

> - Internal restructuring to improve extensibility while preserving public APIs.
> - Addition of the `gatenet.core` module for shared hooks/events.

- Discovery plugin registry (non-breaking):

  - Moved detector classes to `gatenet.discovery.detectors` and introduced a registry in `gatenet.discovery.ssh`.
  - New APIs: `register_detector`, `register_detectors`, `clear_detectors`, `get_detectors` for chain-of-responsibility customization.
  - Backward compatible: existing imports and `_identify_service()` behavior remain unchanged; defaults preserved.

- Hotspot backend abstraction (non-breaking):

  - Added `HotspotBackend` interface and `BackendResult` to enable pluggable platform backends.
  - Introduced platform backends (`gatenet.hotspot.backends.linux`, `gatenet.hotspot.backends.macos`).
  - `Hotspot` now accepts an optional `backend` for dependency injection; legacy behavior remains the default path.

- Core hooks and events (non-breaking):

  - New `gatenet.core` package:
    - `Hooks`: lightweight event bus.
    - `events`: centralized event name constants.
    - `hooks`: shared default Hooks instance for cross-module use.
  - HTTP server now emits lifecycle events and accepts an optional hooks instance:
    - `HTTP_BEFORE_REQUEST`, `HTTP_AFTER_RESPONSE`, `HTTP_ROUTE_NOT_FOUND`, `HTTP_EXCEPTION`.
  - Clients emit send/receive events:
    - TCP: `TCP_BEFORE_SEND`, `TCP_AFTER_RECV`.
    - UDP: `UDP_BEFORE_SEND`, `UDP_AFTER_RECV`.
  - Discovery emits detector chain events in `_identify_service`:
    - `DISCOVERY_BEFORE_DETECT`, `DISCOVERY_AFTER_DETECT`.
  - Diagnostics ping emits events (sync and async):
    - `PING_BEFORE`, `PING_AFTER`.

- Docs & examples:

  - Added a new "Hooks & Events" section to `docs/source/examples.rst` demonstrating HTTP, TCP/UDP, discovery, and diagnostics hook usage.

- Tests:

  - Added tests to verify hook emissions and behavior:
    - Discovery before/after detect hooks.
    - UDP and TCP client before/after hooks.
    - Diagnostics ping before/after hooks.
    - HTTP hooks integration test and a retry helper test mirroring the docs example.

> ###### Notes:
>
> - The detector registry, hotspot backends, and new hooks/events are marked experimental until 1.0 and may evolve with feedback.

### 0.12.4

- Improved error handling in API endpoints to avoid exposing internal error details.
- Fixed the `gatenet.core` module to be able to import and use the new hooks/events.

### 0.12.5

- Fixed broken CLI entry point causing `ModuleNotFoundError: No module named 'gatenet.cli'` when running the `gatenet` console script.
  - Added `gatenet.cli` package and ensured `main` is re-exported from `gatenet.cli`.
  - Aligned module entry (`python -m gatenet.cli`) to `sys.exit(main())` and matched function signature.
- Hardened CLI initialization to avoid optional dependency errors at import time.
  - Refactored CLI to lazy-load subcommand handlers (`iface`, `wifi`, `trace`, `ping`, `dns`, `ports`, `hotspot`).
  - Made `rich` optional; help gracefully falls back to plain text when `rich` isn’t installed.
- Added a `version` subcommand for quick version checks: `gatenet version`.
- Verified console script on macOS with Homebrew Python and editable installs:
  - `gatenet version` prints the package version.
  - `gatenet ping 127.0.0.1 --output plain` executes successfully.

### 0.12.6

Fixed build and dependency issues.

- Added **runtime** dependencies to `pyproject.toml`:
- Added **optional** dependencies for platform-specific and optional features.
- Made Bluetooth imports optional in `discovery/__init__.py`
  - Added try/except blocks around bluetooth imports.
  - Created stub functions that provide helpful error messages when `bleak` is not installed.
  - Maintained the same function signatures to preserve API compatibility.
