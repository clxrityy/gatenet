"""
LoRaRadio: Concrete implementation of RadioInterface for LoRa devices.

Examples:
    >>> from gatenet.radio.lora import LoRaRadio
    >>> radio = LoRaRadio()
    >>> radio.scan_frequencies(868_000_000, 869_000_000, 125)
    >>> radio.on_signal(lambda info: print(info))
"""
from .base import RadioInterface

class LoRaRadio(RadioInterface):
    """LoRa-based radio interface for RF scanning and decoding."""
    def scan_frequencies(self, start_freq: int, end_freq: int, step_khz: int) -> None:
        # Simulate LoRa scan and mesh integration
        for freq in range(start_freq, end_freq, step_khz * 1000):
            info = {"freq": freq, "lora": True, "power": 24}
            self._signal_handler(info)
            # Example: propagate to mesh if available
            try:
                from gatenet.mesh.lora import LoRaRadio as MeshLoRaRadio
                mesh_radio = MeshLoRaRadio()
                mesh_radio.log_rf_signal(info)
                mesh_radio.send_message("RF event", "mesh", frequency=freq, rf_signal=info)
            except Exception:
                pass

    def decode_adsb(self) -> None:
        # LoRa typically does not decode ADS-B, but stub for API consistency
        self._signal_handler({"type": "adsb", "data": None})

    def decode_weather(self) -> None:
        # Stub: Replace with actual weather decoding logic for LoRa
        self._signal_handler({"type": "weather", "data": "LoRa weather packet"})
