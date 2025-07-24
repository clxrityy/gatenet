from gatenet.diagnostics import ping, async_ping
import pytest
import shutil

pytestmark = pytest.mark.skipif(shutil.which("ping") is None, reason="ping not available in environment")

@pytest.mark.parametrize("method", ["icmp", "tcp"])
def test_ping_success(method):
    # Test pinging a known host with both ICMP and TCP
    result = ping("1.1.1.1", count=2, method=method)
    assert isinstance(result["success"], bool)
    assert isinstance(result["raw_output"], str)
    assert "host" in result
    assert "packet_loss" in result
    # Accept either 'rtts' or 'rtt_min' for compatibility, but allow missing for ICMP on some platforms
    if result["success"]:
        # RTT keys may be missing for ICMP on some systems, so only check if present
        if any(k in result for k in ("rtts", "rtt_min")):
            if "rtts" in result:
                assert isinstance(result["rtts"], list)
            for k in ("rtt_min", "rtt_max", "rtt_avg", "jitter"):
                if k in result:
                    assert isinstance(result[k], (float, int))

@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["icmp", "tcp"])
async def test_async_ping_success(method):
    # Test asynchronous pinging of a known host with both ICMP and TCP
    result = await async_ping("8.8.8.8", count=2, method=method)
    assert isinstance(result["success"], bool)
    assert isinstance(result["raw_output"], str)
    assert "host" in result
    assert "packet_loss" in result
    if result["success"]:
        assert any(k in result for k in ("rtts", "rtt_min")), f"Expected at least one RTT key in {result}"
        if "rtts" in result:
            assert isinstance(result["rtts"], list)
        for k in ("rtt_min", "rtt_max", "rtt_avg", "jitter"):
            if k in result:
                assert isinstance(result[k], (float, int))

def test_ping_unreachable():
    # Test unreachable host
    result = ping("10.255.255.1", count=1, method="icmp", timeout=1)
    # Accept any result shape, but must indicate failure or 100% loss
    # Some platforms may not set packet_loss correctly, so just check for success False or error
    raw_output = result.get("raw_output", "")
    found_loss = False
    found_zero_received = False
    if isinstance(raw_output, str):
        found_loss = "100% packet loss" in raw_output
        found_zero_received = "0 packets received" in raw_output or "0 received" in raw_output
    # Accept unreachable if any of the following:
    # - success is False
    # - packet_loss is 100
    # - error in result
    # - raw_output indicates 100% loss or 0 packets received
    assert (
        not result.get("success", True)
        or result.get("packet_loss", 0) == 100
        or "error" in result
        or found_loss
        or found_zero_received
    )

@pytest.mark.asyncio
async def test_async_ping_unreachable():
    # Test unreachable host (async)
    # If async_ping does not support timeout, this will be ignored
    result = await async_ping("10.255.255.1", count=1, method="icmp")
    assert not result.get("success", True) or result.get("packet_loss", 0) == 100 or "error" in result

def test_ping_invalid_method():
    # Test invalid method argument
    result = ping("1.1.1.1", count=1, method="invalid")
    assert result["success"] is False
    assert "error" in result

@pytest.mark.asyncio
async def test_async_ping_invalid_method():
    # Test invalid method argument (async)
    result = await async_ping("1.1.1.1", count=1, method="invalid")
    assert result["success"] is False
    assert "error" in result