from gatenet.cli.scan import run_scan


def test_run_scan_basic(capsys):
    run_scan("example.com", json_output=False)
    captured = capsys.readouterr()
    target = captured.out.splitlines()[1]
    open_ports = captured.out.splitlines()[3:]
    assert "example.com" in target
    assert any("22" in line and "ssh" in line for line in open_ports)
    assert any("80" in line and "http" in line for line in open_ports)
