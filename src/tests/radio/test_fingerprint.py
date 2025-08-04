"""
Test RF fingerprinting and FFT feature extraction for SDRRadio.
"""
import pytest
import numpy as np
from gatenet.radio.sdr import SDRRadio

def test_sdrradio_fft_feature():
    radio = SDRRadio()
    samples = radio.get_samples()
    fft = np.fft.fft(samples)
    assert isinstance(fft, np.ndarray)
    assert fft.size == samples.size
    assert np.isfinite(fft).all()
