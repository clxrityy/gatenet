"""
RadioInterface: Abstract base for SDR/LoRa/ESP/Weather RF integration.

Examples:
    >>> radio = RadioInterface()
    >>> radio.scan_frequencies(433_000_000, 434_000_000, 10)
    >>> radio.on_signal(lambda info: print(info))

See: https://github.com/clxrityy/gatenet
"""
from typing import Callable, Any

class RadioInterface:
    """Base class for RF radio integration (SDR, LoRa, ESP, Weather).

    Args:
        device_path (str): Path to SDR/LoRa/ESP device.
        sample_rate (int): Sample rate in Hz.

    Example:
        >>> radio = RadioInterface()
        >>> radio.scan_frequencies(433_000_000, 434_000_000, 10)
        >>> radio.on_signal(lambda info: print(info))
    """
    def __init__(self, device_path: str = "/dev/rtl_sdr", sample_rate: int = 2_000_000) -> None:
        self.device_path = device_path
        self.sample_rate = sample_rate
        self._signal_handler: Callable[[Any], None] = lambda info: None

    def scan_frequencies(self, start_freq: int, end_freq: int, step_khz: int) -> None:
        """Sweep a frequency range and detect power peaks or anomalies.

        Args:
            start_freq (int): Start frequency in Hz.
            end_freq (int): End frequency in Hz.
            step_khz (int): Step size in kHz.
        """
        pass

    def decode_adsb(self) -> None:
        """Decode ADS-B aircraft messages from 1090 MHz."""
        pass

    def decode_weather(self) -> None:
        """Decode weather station signals (e.g. 433 MHz devices)."""
        pass

    def on_signal(self, handler: Callable[[Any], None]) -> None:
        """Register callback for signal detection.

        Args:
            handler (Callable): Function to call with signal info.
        """
        self._signal_handler = handler
