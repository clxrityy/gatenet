Security Guidelines
===================

Networking tools and hotspot management require careful defaults and hygiene.

Defaults & recommendations
--------------------------

- Prefer WPA2/WPA3 for hotspots; avoid OPEN unless you fully understand the risks
- Enforce strong passwords (12+ chars) and recommend `generate-password`
- Validate and sanitize user input in CLI and HTTP routes
- Least-privilege: only elevate when required (hotspot start/stop)

Threat considerations
---------------------

- Injection through crafted network data or CLI args
- SSRF/CSRF risks in HTTP microservices; lock down origins and routes
- Untrusted plugins: only install signed or reviewed packages

Operational practices
---------------------

- Documented deprecation and change policy to avoid surprise breakage
- Security audit/review before 1.0; consider community bug bounty
- Rotate hotspot credentials and monitor connected devices

Report issues
-------------

If you discover a vulnerability, please open a private security advisory on GitHub or email the maintainer listed in the project metadata.
