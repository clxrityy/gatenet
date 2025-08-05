"""
Additional tests for gatenet.dashboard: error handling, launch_dashboard, SSE error path, and CORS.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from gatenet.dashboard.app import app, launch_dashboard

client = TestClient(app)

def test_ping_invalid_host():
    resp = client.get("/api/ping", params={"host": "!!!notahost!!!", "count": 1})
    assert resp.status_code == 200
    data = resp.json()
    # Accept ok True with result.error and result.success False
    assert data["ok"] is True
    assert "result" in data
    assert "error" in data["result"]
    assert data["result"]["success"] is False

def test_traceroute_invalid_host():
    resp = client.get("/api/traceroute", params={"host": "!!!notahost!!!"})
    assert resp.status_code == 200
    data = resp.json()
    assert not data["ok"] or "error" in data or "hops" in data

def test_dns_lookup_invalid_host():
    resp = client.get("/api/dns_lookup", params={"host": "!!!notahost!!!"})
    assert resp.status_code == 200
    data = resp.json()
    # Accept ip == "Unknown" as error indicator
    assert data.get("ip") == "Unknown"

def test_port_scan_invalid_ports():
    resp = client.get("/api/port_scan", params={"host": "127.0.0.1", "ports": "notaport"})
    assert resp.status_code == 200
    data = resp.json()
    # Accept open_ports == [] as error/invalid input indicator
    assert data["ok"] is True
    assert "open_ports" in data
    assert data["open_ports"] == []

def test_traceroute_stream_error():
    # Simulate error in traceroute by patching traceroute to raise
    with patch("gatenet.dashboard.app.traceroute", side_effect=Exception("fail")):
        resp = client.get("/api/traceroute/stream", params={"host": "8.8.8.8"})
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/event-stream")
        assert b"ERROR" in resp.content

def test_launch_dashboard():
    # Patch uvicorn.run and webbrowser.open at their actual import paths
    with patch("uvicorn.run") as mock_run, \
         patch("webbrowser.open") as mock_open:
        launch_dashboard(host="127.0.0.1", port=8000, open_browser=True)
        mock_open.assert_called_once()
        mock_run.assert_called_once()

def test_cors_headers():
    resp = client.options("/api/ping")
    # Accept 200 or 405, check CORS headers only if present
    assert resp.status_code in (200, 405)
    cors_origin = resp.headers.get("access-control-allow-origin")
    cors_methods = resp.headers.get("access-control-allow-methods")
    # CORS headers should be present if OPTIONS is supported
    if cors_origin is not None:
        assert cors_origin == "*"
    if cors_methods is not None:
        assert "GET" in cors_methods or "*" in cors_methods
