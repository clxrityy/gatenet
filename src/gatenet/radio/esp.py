"""
ESPRadio: Concrete implementation of RadioInterface for ESP-based mesh radios.

Examples:
    >>> from gatenet.radio.esp import ESPRadio
    >>> radio = ESPRadio()
    >>> radio.scan_frequencies(2400_000_000, 2483_500_000, 1000)
    >>> radio.on_signal(lambda info: print(info))
"""
from .base import RadioInterface

class ESPRadio(RadioInterface):
    """ESP-based radio interface for Wi-Fi mesh scanning and decoding."""
    def scan_frequencies(self, start_freq: int, end_freq: int, step_khz: int) -> None:
        # Simulate ESP scan and mesh integration
        for freq in range(start_freq, end_freq, step_khz * 1000):
            info = {"freq": freq, "esp": True, "power": 18}
            self._signal_handler(info)
            # Example: propagate to mesh if available
            try:
                from gatenet.mesh.esp import ESPRadio as MeshESPRadio
                mesh_radio = MeshESPRadio()
                mesh_radio.log_rf_signal(info)
                mesh_radio.send_message("RF event", "mesh", channel=freq, rf_signal=info)
            except Exception:
                pass

    def decode_adsb(self) -> None:
        # ESP typically does not decode ADS-B, but stub for API consistency
        self._signal_handler({"type": "adsb", "data": None})

    def decode_weather(self) -> None:
        # Stub: Replace with actual weather decoding logic for ESP
        self._signal_handler({"type": "weather", "data": "ESP weather packet"})
