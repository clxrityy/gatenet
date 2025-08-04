"""
SDRRadio: Concrete implementation of RadioInterface for SDR devices.

Examples:
    >>> from gatenet.radio.sdr import SDRRadio
    >>> radio = SDRRadio()
    >>> radio.scan_frequencies(433_000_000, 434_000_000, 10)
    >>> radio.on_signal(lambda info: print(info))
"""
import numpy as np
from .base import RadioInterface

class SDRRadio(RadioInterface):
    def get_samples(self, size: int = 1024) -> "np.ndarray":
        """Return simulated SDR samples as a NumPy array (for testing/visualization)."""
        try:
            import numpy as np
        except ImportError:
            raise RuntimeError("numpy is required for get_samples")
        # Simulate random samples for testing using numpy's Generator
        rng = np.random.default_rng(seed=42)
        return rng.normal(0, 1, size)

    def detect_collisions(self) -> list:
        """Return a simulated list of RF collisions (for testing)."""
        # Simulate two collisions for test coverage
        return [
            {"source": "deviceA", "strength": -65.0},
            {"source": "deviceB", "strength": -70.5}
        ]
    """SDR-based radio interface for RF scanning and decoding."""
    def scan_frequencies(self, start_freq: int, end_freq: int, step_khz: int) -> None:
        # Simulate SDR scan and mesh integration
        for freq in range(start_freq, end_freq, step_khz * 1000):
            info = {"freq": freq, "sdr": True, "power": 42}
            self._signal_handler(info)
            # Example: propagate to mesh if available
            try:
                from gatenet.mesh.radio import MeshRadio
                mesh_radio = MeshRadio()
                mesh_radio.log_rf_signal(info)
                mesh_radio.send_message("RF event", "mesh", rf_signal=info)
            except Exception:
                pass

    def decode_adsb(self) -> None:
        # Stub: Replace with actual ADS-B decoding logic
        self._signal_handler({"type": "adsb", "data": "aircraft detected"})

    def decode_weather(self) -> None:
        # Stub: Replace with actual weather decoding logic
        self._signal_handler({"type": "weather", "data": "weather station signal"})
