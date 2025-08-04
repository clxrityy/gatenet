"""
Test ESPRadio functionality and event callbacks.
"""
import pytest
from gatenet.radio.esp import ESPRadio

@pytest.mark.asyncio
async def test_scan_frequencies_event():
    results = []
    def handler(info):
        results.append(info)
    radio = ESPRadio()
    radio.on_signal(handler)
    radio.scan_frequencies(2400_000_000, 2401_000_000, 1000)
    assert any(r["esp"] for r in results)

@pytest.mark.asyncio
async def test_decode_weather_event():
    results = []
    def handler(info):
        results.append(info)
    radio = ESPRadio()
    radio.on_signal(handler)
    radio.decode_weather()
    assert any(r["type"] == "weather" for r in results)
