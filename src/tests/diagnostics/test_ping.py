from gatenet.diagnostics import ping, async_ping
import pytest

@pytest.mark.parametrize("method", ["icmp", "tcp"])
def test_ping_success(method):
    # Test pinging a known host with both ICMP and TCP
    result = ping("1.1.1.1", count=2, method=method)
    assert isinstance(result["success"], bool)
    assert isinstance(result["raw_output"], str)
    assert "host" in result
    assert "packet_loss" in result
    assert "rtts" in result
    if result["success"]:
        assert "rtt_min" in result
        assert "rtt_max" in result
        assert "rtt_avg" in result
        assert "jitter" in result
        assert isinstance(result["rtts"], list)

@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["icmp", "tcp"])
async def test_async_ping_success(method):
    # Test asynchronous pinging of a known host with both ICMP and TCP
    result = await async_ping("8.8.8.8", count=2, method=method)
    assert isinstance(result["success"], bool)
    assert isinstance(result["raw_output"], str)
    assert "host" in result
    assert "packet_loss" in result
    assert "rtts" in result
    if result["success"]:
        assert "rtt_min" in result
        assert "rtt_max" in result
        assert "rtt_avg" in result
        assert "jitter" in result
        assert isinstance(result["rtts"], list)

def test_ping_unreachable():
    # Test unreachable host
    result = ping("10.255.255.1", count=1, method="icmp")
    assert result["success"] is False or result["packet_loss"] == 100
    assert "error" in result or result["packet_loss"] == 100

@pytest.mark.asyncio
async def test_async_ping_unreachable():
    # Test unreachable host (async)
    result = await async_ping("10.255.255.1", count=1, method="icmp")
    assert result["success"] is False or result["packet_loss"] == 100
    assert "error" in result or result["packet_loss"] == 100

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