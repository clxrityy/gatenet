from gatenet.diagnostics import ping

def test_ping():
    # Test pinging a known host
    result = ping("8.8.8.8", count=1)
    assert result["success"] is True, "Ping to 8.8.8.8 should succeed"