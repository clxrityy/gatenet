"""
Test spectrogram visualization and sample generation for SDRRadio.
"""
import pytest
import numpy as np
from gatenet.radio.sdr import SDRRadio

def test_sdrradio_get_samples_shape():
    radio = SDRRadio()
    samples = radio.get_samples()
    assert isinstance(samples, np.ndarray)
    assert samples.ndim == 1
    assert samples.size > 0

def test_sdrradio_specgram(monkeypatch):
    radio = SDRRadio()
    rng = np.random.default_rng(42)  # Fixed seed for reproducibility
    samples = rng.normal(0, 1, 1024)
    monkeypatch.setattr(radio, "get_samples", lambda: samples)
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        pytest.skip("matplotlib not installed")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Convert ndarray to list for specgram compatibility
    ax.specgram(samples.tolist(), NFFT=256, Fs=2_000_000)
    plt.close(fig)
