from gatenet.diagnostics import ping

def test_ping():
    # Test pinging a known host
    try:
        result = ping("1.1.1.1", count=1)
    except Exception as e:
        assert False, f"Ping to 1.1.1.1 failed: {e}"
    assert result["success"] is True, "Ping to 1.1.1.1 should succeed"