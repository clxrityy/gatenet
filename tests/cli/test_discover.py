from gatenet.cli.discover import run_discover


def test_run_discover_basic(capsys):
    run_discover(json_output=False)
    captured = capsys.readouterr()
    print(captured.out)
    assert "ip=" in captured.out
    assert "hostname=" in captured.out
