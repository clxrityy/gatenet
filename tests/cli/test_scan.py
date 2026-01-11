import json

import gatenet.cli.scan as scan_cli
from gatenet.core.models import Port, ScanResult


def test_run_scan_outputs_json(monkeypatch, capsys):
    # Arrange: avoid real sockets by stubbing scan_target used inside scan_cli.run_scan
    def fake_scan_target(target: str, ports) -> ScanResult:
        assert target == "localhost"
        assert list(ports) == [22, 80, 443]
        return ScanResult(
            target=target,
            open_ports=[
                Port(number=22, protocol="tcp", service="ssh"),
                Port(number=80, protocol="tcp", service="http"),
            ],
        )

    monkeypatch.setattr(scan_cli, "scan_target", fake_scan_target)

    # Act
    scan_cli.run_scan("localhost", ports=[22, 80, 443], json_output=True)

    # Assert: JSON is stable/easy to validate
    out = capsys.readouterr().out
    payload = json.loads(out)

    assert payload["target"] == "localhost"
    assert [p["number"] for p in payload["open_ports"]] == [22, 80]
    assert {p["service"] for p in payload["open_ports"]} == {"ssh", "http"}


def test_run_scan_outputs_human_readable(monkeypatch, capsys):
    # Arrange: avoid real sockets by stubbing scan_target used inside scan_cli.run_scan
    def fake_scan_target(target: str, ports) -> ScanResult:
        assert target == "localhost"
        assert list(ports) == [22, 80, 443]
        return ScanResult(
            target=target,
            open_ports=[
                Port(number=22, protocol="tcp", service="ssh"),
                Port(number=80, protocol="tcp", service="http"),
            ],
        )

    monkeypatch.setattr(scan_cli, "scan_target", fake_scan_target)

    # Act
    scan_cli.run_scan("localhost", ports=[22, 80, 443], json_output=False)

    # Assert: human-readable output contains expected lines
    out = capsys.readouterr().out

    assert "localhost" in out
    assert ("22" and "ssh") in out
    assert ("80" and "http") in out
