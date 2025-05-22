# GATENET — CHANGELOG

## OUTLINE

- [v0](#v0) (BETA)
    - [0.1.0](#010)
    - [0.1.1](#011)
    - [0.1.2](#012)

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

## 0.1.2

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
    - Verfies status routes, echo routes, and default error handling.