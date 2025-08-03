# Contributing to gatenet

#

<!-- Key Resources & Links -->

| **Resources**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | **CLI Resources**                                                                                                                                                                                                                                                                                                                                                                                          | **Developer / Contributor Resources**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a href="https://gatenet.readthedocs.io/"><img src="https://img.shields.io/badge/docs-readthedocs-blue?logo=readthedocs&style=for-the-badge" alt="Documentation" /></a> <a href="https://gatenet.readthedocs.io/en/latest/changelog.html"><img src="https://img.shields.io/badge/changelog-latest-blueviolet?logo=markdown&style=for-the-badge" alt="Changelog" /></a> <a href="https://pypi.org/project/gatenet/"><img src="https://img.shields.io/pypi/v/gatenet?label=PyPI&logo=pypi&style=for-the-badge" alt="PyPI" /></a> <a href="https://gatenet.readthedocs.io/en/latest/architecture.html"><img src="https://img.shields.io/badge/architecture-overview-green?logo=github&style=for-the-badge" alt="Architecture Overview" /></a> <a href="https://gatenet.readthedocs.io/en/latest/hardware.html"><img src="https://img.shields.io/badge/hardware-setup-orange?logo=raspberrypi&style=for-the-badge" alt="Hardware Setup" /></a> | <a href="https://gatenet.readthedocs.io/en/latest/cli.html"><img src="https://img.shields.io/badge/cli-usage-blue?logo=terminal&style=for-the-badge" alt="CLI Usage" /></a> <a href="https://gatenet.readthedocs.io/en/latest/cli_integration_examples.html"><img src="https://img.shields.io/badge/cli-integration%20examples-teal?logo=python&style=for-the-badge" alt="CLI Integration Examples" /></a> | <a href="https://github.com/clxrityy/gatenet/blob/master/.github/CONTRIBUTING.md"><img src="https://img.shields.io/badge/contributing-guidelines-yellow?logo=github&style=for-the-badge" alt="Contributing Guidelines" /></a> <a href="https://github.com/clxrityy/gatenet/blob/master/.github/CODE_OF_CONDUCT.md"><img src="https://img.shields.io/badge/code%20of%20conduct-enforced-red?logo=github&style=for-the-badge" alt="Code of Conduct" /></a> <a href="https://github.com/clxrityy/gatenet/blob/master/.github/SECURITY.md"><img src="https://img.shields.io/badge/security-policy-critical?logo=github&style=for-the-badge" alt="Security Policy" /></a> |

Thank you for considering contributing to gatenet! Your help is appreciated. This guide will help you understand the project structure, development workflow, and best practices for making contributions.

---

## Project Architecture

**gatenet** is a modular Python networking toolkit for diagnostics, service discovery, mesh networking, and robust socket/HTTP microservices. The codebase is organized as follows:

- `src/gatenet/` — Main package code
  - `client/` — TCP, UDP, and HTTP clients (sync and async)
  - `socket/` — TCP and UDP socket servers (low-level, connection-oriented)
  - `http_/` — HTTP server and client (sync and async, built on `http.server`, `urllib`, and `aiohttp`)
  - `diagnostics/` — Tools for ping, traceroute, bandwidth, geo IP, DNS, port scanning
  - `discovery/` — Service discovery using strategy and chain-of-responsibility patterns (SSH, HTTP, FTP, SMTP, mDNS, Bluetooth, UPNP, etc.)
  - `mesh/` — Modular mesh networking (LoRa, ESP, Wi-Fi, GPS, SDR integration, encrypted messaging, topology mapping)
  - `dashboard/` — FastAPI-based web dashboard for diagnostics and live output (SSE)
  - `utils/` — Utilities (e.g., `get_free_port()`)
- `src/tests/` — Unit and integration tests, mirroring the main package structure
- `examples/` — Example scripts for diagnostics, discovery, HTTP, TCP/UDP, mesh, and dashboard usage
- `docs/` — Sphinx documentation, with automated coverage summary
- `Makefile` — Automation for testing, coverage, docs, and release

### Design Patterns

- **Strategy Pattern**: Used for service detectors (e.g., SSH, HTTP, FTP, SMTP)
- **Chain of Responsibility**: Service identification tries detectors in sequence
- **Abstract Base Classes (ABC)**: For extensible interfaces
- **Async/Await**: Async support for HTTP, ping, and more

---

## Development Workflow & Makefile Scripts

The Makefile provides all the scripts you need for development:

- `make venv` — Create a Python virtual environment
- `make install` — Install all dependencies (core, dev, docs)
- `make test` — Run all tests with pytest
- `make coverage` — Run tests and generate HTML and XML coverage reports
- `make badge` — Generate a coverage badge (SVG)
- `make coverage-copy` — Copy HTML coverage report into docs static directory
- `make coverage-summary` — Generate a coverage summary table for docs (from coverage.xml)
- `make docs` — Build Sphinx documentation (runs coverage, badge, summary, and builds HTML docs)
- `make clean` — Remove build, dist, coverage, and doc artifacts
- `make build` — Build the package (wheel and sdist)
- `make publish` — Upload to PyPI (or TestPyPI if `TESTPYPI=1`)
- `make release` — Clean, build, test, docs, and publish for a full release

**Tip:** Use `make help` to see all available targets.

---

## How to Contribute

1. **Fork the repository** and create your branch from `master`.
2. **Write clear, modular code** following the project’s structure and coding standards (see below).
3. **Add or update tests** for your changes (unit and/or integration as appropriate).
4. **Document your code** with Google-style or NumPy-style docstrings.
5. **Update the README, docs, or examples** if your change affects usage or features.
6. **Run all tests and ensure they pass** (`make test`).
7. **Build the docs and check coverage** (`make docs`).
8. **Submit a pull request** with a clear description of your changes and reference any related issues.

---

## Coding Standards & Best Practices

- Follow the [Gatenet Copilot Instructions](.github/copilot-instructions.md) for architecture, patterns, and style.
- Use method chaining for fluent APIs where appropriate.
- Use abstract base classes (ABC) for extensible interfaces.
- Use strategy and chain-of-responsibility patterns for service discovery and extensible features.
- Return Python `dict` (not serialized JSON) from HTTP routes.
- Include type hints and docstrings for all public functions and classes.
- Prefer async/await for new async features.

---

## Testing

- Use `pytest` and `assert` for all tests.
- Place tests in the appropriate subdirectory under `src/tests/`.
- Use `get_free_port()` from `gatenet.utils.net` to avoid port conflicts in tests.
- Use `pytest.mark.asyncio` for async tests.
- Mock network connections with `unittest.mock` or `pytest` fixtures.
- Test both positive and negative cases, including edge cases (timeouts, empty responses, case sensitivity).
- Run `make test` before submitting a PR.

---

## Examples & Documentation

- See the `examples/` directory for practical scripts covering diagnostics, discovery, HTTP, TCP/UDP, and dashboard usage.
- Add or update examples if you introduce new features or patterns.
- Documentation is built with Sphinx (`make docs`).
- Coverage summary is auto-generated and included in the docs.

---

## Submitting a Pull Request

- Ensure your branch is up to date with `main`.
- Run all tests locally with `pytest` and ensure they pass.
- Build the docs and check for warnings or errors.
- Add a descriptive title and summary to your pull request.
- Reference any related issues in your pull request description.

---

## Reporting Issues

- Use [GitHub Issues](https://github.com/clxrityy/gatenet/issues) to report bugs or request features.
- Include as much detail as possible: environment, steps to reproduce, expected and actual behavior.

---

## Code of Conduct

Be respectful and constructive. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) if present.

---

Thank you for helping make gatenet better!
