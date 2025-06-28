# Contributing to gatenet

Thank you for considering contributing to gatenet! Your help is appreciated. Please follow these guidelines to ensure a smooth contribution process.

---

## How to Contribute

1. **Fork the repository** and create your branch from `main`.
2. **Write clear, modular code** following the project’s structure and coding standards.
3. **Add or update tests** for your changes.
4. **Document your code** with Google-style or NumPy-style docstrings.
5. **Update the README or relevant docs** if your change affects usage or features.
6. **Submit a pull request** with a clear description of your changes.

---

## Coding Standards

- Follow the [Gatenet Copilot Instructions](.github/copilot-instructions.md).
- Use method chaining where appropriate for fluent APIs.
- Use abstract base classes (ABC) for extensible interfaces.
- Use the strategy and chain-of-responsibility patterns for service discovery and similar extensible features.
- When returning JSON from HTTP routes, return a Python `dict` (not serialized JSON).
- Include type hints and docstrings for all public functions and classes.

---

## Testing

- Use `pytest` and `assert` for all tests.
- Place tests in the appropriate subdirectory under `src/tests/`.
- Use `get_free_port()` from `gatenet.utils.net` to avoid port conflicts in tests.
- Use `pytest.mark.asyncio` for async tests.
- Mock network connections with `unittest.mock` or `pytest` fixtures.
- Test both positive and negative cases, including edge cases (timeouts, empty responses, case sensitivity).

---

## Submitting a Pull Request

- Ensure your branch is up to date with `main`.
- Run all tests locally with `pytest` and ensure they pass.
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

Thank you for helping
