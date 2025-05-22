# src/tests/http/test_http_client.py

import json
import time
import threading
from gatenet.http.base import HTTPServerComponent
from gatenet.http.client import HTTPClient
from gatenet.utils.net import get_free_port



def test_http_client_basic_get_and_post():
    host = "127.0.0.1"
    port = get_free_port()
    server = HTTPServerComponent(host=host, port=port)

    @server.route("/echo", method="POST")
    def echo(_req, data):
        return {
            "received": data
        }
    
    @server.route("/status")
    def status(_req):
        return {
            "ok": True
        }
    
    server.start()
    time.sleep(0.5)  # Give the server a moment to start
    

    client = HTTPClient(f"http://{host}:{port}")

    # Test GET
    status_response = client.get("/status")
    assert status_response == {"ok": True}

    # Test POST
    echo = client.post("/echo", {"foo": "bar"}, headers={"Content-Type": "application/json"})
    assert echo == {"received": {"foo": "bar"}}

    server.stop()
