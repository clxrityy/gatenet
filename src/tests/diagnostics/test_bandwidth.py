import pytest
from gatenet.diagnostics.bandwidth import measure_bandwidth
import socket
import threading
import time

class DummyBandwidthServer(threading.Thread):
    """A simple TCP server for bandwidth testing (echoes or sends data)."""
    def __init__(self, host="127.0.0.1", port=0, mode="download", payload_size=65536):
        super().__init__()
        self.host = host
        self.port = port
        self.mode = mode
        self.payload_size = payload_size
        self._stop = threading.Event()
        self._server = None
        self.actual_port = None

    def run(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self.actual_port = self._server.getsockname()[1]
        self._server.listen(1)
        conn, _ = self._server.accept()
        try:
            if self.mode == "download":
                payload = b"1" * self.payload_size
                while not self._stop.is_set():
                    try:
                        conn.sendall(payload)
                    except Exception:
                        break
            else:  # upload
                while not self._stop.is_set():
                    data = conn.recv(self.payload_size)
                    if not data:
                        break
        finally:
            conn.close()
            self._server.close()

    def stop(self):
        self._stop.set()
        # Connect to self to unblock accept
        if self.actual_port is not None:
            try:
                s = socket.create_connection((self.host, self.actual_port), timeout=1)
                s.close()
            except Exception:
                pass
        self.join()

def test_measure_bandwidth_download():
    server = DummyBandwidthServer(mode="download")
    server.start()
    while server.actual_port is None:
        time.sleep(0.01)
    result = measure_bandwidth("127.0.0.1", port=server.actual_port, duration=1.0, direction="download")
    server.stop()
    assert result["bandwidth_mbps"] > 0
    assert result["bytes_transferred"] > 0
    assert result["duration"] > 0

def test_measure_bandwidth_upload():
    server = DummyBandwidthServer(mode="upload")
    server.start()
    while server.actual_port is None:
        time.sleep(0.01)
    result = measure_bandwidth("127.0.0.1", port=server.actual_port, duration=1.0, direction="upload")
    server.stop()
    assert result["bandwidth_mbps"] > 0
    assert result["bytes_transferred"] > 0
    assert result["duration"] > 0

def test_invalid_direction():
    with pytest.raises(AssertionError):
        measure_bandwidth("127.0.0.1", direction="sideways")
