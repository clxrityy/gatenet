"""
Test MeshRadio log archival via sync_logs().
"""
import os
import json
import tempfile
import pytest
from gatenet.mesh.radio import MeshRadio

def test_sync_logs_creates_file_and_content():
    radio = MeshRadio()
    radio.log_gps(51.5074, -0.1278)
    radio.log_rf_signal({"freq": 868000000, "power": 24, "type": "lora"})
    radio.scan_wifi(mock=True)
    radio.send_message("Hello", "node2")
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "mesh_radio_logs.json")
        result = radio.sync_logs(file_path)
        assert result is True
        assert os.path.exists(file_path)
        with open(file_path) as f:
            logs = json.load(f)
        assert "packets" in logs
        assert "topology" in logs
        assert "gps_location" in logs
        assert "rf_signal" in logs
        assert "wifi_networks" in logs
        assert logs["packets"]
        assert logs["topology"]["locations"]
        assert logs["topology"]["signals"]
        assert logs["wifi_networks"]

def test_sync_logs_handles_error(monkeypatch):
    radio = MeshRadio()
    # Simulate error by monkeypatching open to raise exception
    def raise_ioerror(*a, **kw):
        raise IOError("fail")
    monkeypatch.setattr("builtins.open", raise_ioerror)
    result = radio.sync_logs("/tmp/should_fail.json")
    assert result is False
