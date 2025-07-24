"""
Integration tests for gatenet: HTTP server, client, and diagnostics working together.

Covers end-to-end request/response, diagnostics, and error handling.
"""

import time
import pytest
import shutil
from gatenet.http_.server import HTTPServerComponent
from gatenet.http_.client import HTTPClient
from gatenet.diagnostics.ping import ping
from gatenet.utils.net import get_free_port


pytestmark = pytest.mark.skipif(shutil.which("ping") is None, reason="ping not available in environment")


@pytest.mark.integration
def test_http_server_client_ping(tmp_path):
    """Test HTTP server and client integration with diagnostics (ping)."""
    port = get_free_port()
    server = HTTPServerComponent(host="127.0.0.1", port=port)

    @server.route("/status", method="GET")
    def status_handler(req):
        return {"ok": True}

    server.start()
    time.sleep(0.2)  # Wait for server to start

    client = HTTPClient(f"http://127.0.0.1:{port}")
    response = client.get("/status")  # type: ignore[attr-defined]
    assert response["ok"] is True or response["data"]["ok"] is True

    # Diagnostics: ping the server
    ping_result = ping("127.0.0.1")
    assert ping_result["success"] is True

    server.stop()


@pytest.mark.integration
def test_http_server_client_error_handling(tmp_path):
    """Test HTTP server and client integration with error handling (404)."""
    port = get_free_port()
    server = HTTPServerComponent(host="127.0.0.1", port=port)
    server.start()
    time.sleep(0.2)

    client = HTTPClient(f"http://127.0.0.1:{port}")
    response = client.get("/notfound")  # type: ignore[attr-defined]
    assert response["ok"] is False
    assert response["status"] == 404
    server.stop()
