"""
Edge case tests for ping and async_ping.
"""
import pytest
from gatenet.diagnostics.ping import ping, async_ping
import asyncio

def test_ping_invalid_host():
    result = ping("invalid.host")
    assert isinstance(result, dict)
    assert result.get("success", False) is False or result.get("avg_ms", 0) == 0

def test_ping_zero_count():
    result = ping("8.8.8.8", count=0)
    assert isinstance(result, dict)
    assert result.get("count", 0) == 0 or result.get("success", False) is False

@pytest.mark.asyncio
async def test_async_ping_invalid_host():
    result = await async_ping("invalid.host")
    assert isinstance(result, dict)
    assert result.get("success", False) is False or result.get("avg_ms", 0) == 0

@pytest.mark.asyncio
async def test_async_ping_zero_count():
    result = await async_ping("8.8.8.8", count=0)
    assert isinstance(result, dict)
    assert result.get("count", 0) == 0 or result.get("success", False) is False
