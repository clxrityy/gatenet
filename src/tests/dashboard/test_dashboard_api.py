"""
Tests for gatenet.dashboard FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from gatenet.dashboard.app import app

client = TestClient(app)

def test_index():
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Gatenet Dashboard" in resp.content

def test_ping():
    resp = client.get("/api/ping", params={"host": "8.8.8.8", "count": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert "ok" in data
    assert "result" in data or "error" in data

def test_traceroute():
    resp = client.get("/api/traceroute", params={"host": "8.8.8.8"})
    assert resp.status_code == 200
    data = resp.json()
    assert "ok" in data
    assert "hops" in data or "error" in data

def test_dns_lookup():
    resp = client.get("/api/dns_lookup", params={"host": "google.com"})
    assert resp.status_code == 200
    data = resp.json()
    assert "ok" in data
    assert "ip" in data or "error" in data

def test_port_scan():
    resp = client.get("/api/port_scan", params={"host": "127.0.0.1", "ports": "22,80"})
    assert resp.status_code == 200
    data = resp.json()
    assert "ok" in data
    assert "open_ports" in data or "error" in data

def test_traceroute_stream():
    resp = client.get("/api/traceroute/stream", params={"host": "8.8.8.8"})
    assert resp.status_code == 200
    # Should be an event stream (text/event-stream)
    assert resp.headers["content-type"].startswith("text/event-stream")
    # Read a few lines from the stream
    lines = []
    for line in resp.content.splitlines():
        if line:
            lines.append(line)
        if len(lines) > 2:
            break
    assert any(b"data:" in l for l in lines)
