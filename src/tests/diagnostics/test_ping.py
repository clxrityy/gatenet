from gatenet.diagnostics import ping

def test_ping():
    # Test pinging a known host
    result = ping("1.1.1.1", count=1)
    assert result["success"] is True, "Ping to 1.1.1.1 should succeed"