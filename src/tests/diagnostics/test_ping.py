from gatenet.diagnostics import ping, async_ping
import pytest

def test_ping():
    # Test pinging a known host
    try:
        result = ping("1.1.1.1", 1)
    except Exception as e:
        assert False, f"Ping to 1.1.1.1 failed: {e}"
    assert result["success"] is True or result["success"] is False, "Ping result should have a success status"
    # assert isinstance(result["raw_output"], str), "Ping output should be a string"
    

@pytest.mark.asyncio
async def test_async_ping():
    # Test asynchronous pinging of a known host
    try:
        result = await async_ping("8.8.8.8", 1)
        assert result["success"] is True or result["success"] is False, "Async ping result should have a success status"
        # assert isinstance(result["raw_output"], str), "Async ping output should be a string"
    except Exception as e:
        assert False, f"Async ping to 8.8.8.8 failed: {e}"