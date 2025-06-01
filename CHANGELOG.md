# GATENET — CHANGELOG

## OUTLINE

- [v0](#v0) (BETA)
    - [0.1.0](#010)
        - [0.1.1](#011)
    - [0.3.0](#030)
        - [0.3.2](#032)
    - [0.4.0](#040)

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
