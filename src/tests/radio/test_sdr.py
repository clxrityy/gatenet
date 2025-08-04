"""
Test SDRRadio functionality and event callbacks.
"""
import pytest
from gatenet.radio.sdr import SDRRadio

@pytest.mark.asyncio
async def test_scan_frequencies_event():
    results = []
    def handler(info):
        results.append(info)
    radio = SDRRadio()
    radio.on_signal(handler)
    radio.scan_frequencies(433_000_000, 433_010_000, 10)
    assert any(r["freq"] == 433_000_000 for r in results)

@pytest.mark.asyncio
async def test_decode_adsb_event():
    results = []
    def handler(info):
        results.append(info)
    radio = SDRRadio()
    radio.on_signal(handler)
    radio.decode_adsb()
    assert any(r["type"] == "adsb" for r in results)

@pytest.mark.asyncio
async def test_decode_weather_event():
    results = []
    def handler(info):
        results.append(info)
    radio = SDRRadio()
    radio.on_signal(handler)
    radio.decode_weather()
    assert any(r["type"] == "weather" for r in results)
