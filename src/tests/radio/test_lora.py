"""
Test LoRaRadio functionality and event callbacks.
"""
import pytest
from gatenet.radio.lora import LoRaRadio

@pytest.mark.asyncio
async def test_scan_frequencies_event():
    results = []
    def handler(info):
        results.append(info)
    radio = LoRaRadio()
    radio.on_signal(handler)
    radio.scan_frequencies(868_000_000, 868_125_000, 125)
    assert any(r["lora"] for r in results)

@pytest.mark.asyncio
async def test_decode_weather_event():
    results = []
    def handler(info):
        results.append(info)
    radio = LoRaRadio()
    radio.on_signal(handler)
    radio.decode_weather()
    assert any(r["type"] == "weather" for r in results)
