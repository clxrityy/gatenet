import pytest
from gatenet.http.server import HTTPServerComponent
from gatenet.http.async_client import AsyncHTTPClient
from gatenet.utils.net import get_free_port
import json
import time

@pytest.mark.asyncio
async def test_async_http_client_get_and_post():
    host = "127.0.0.1"
    port = get_free_port()
    server = HTTPServerComponent(host=host, port=port)
    
    @server.route("/status", method="GET")
    def status_handler(_req):
        return {
            "ok": True,
        }
    
    @server.route("/echo", method="POST")
    def echo_handler(req):
        length = int(req.headers.get("Content-Length", 0))
        body = req.rfile.read(length)
        data = json.loads(body)
        
        return {
            "received": data,
        }
        
    server.start()
    time.sleep(0.3) # Wait for the server to start
    
    client = AsyncHTTPClient(f"http://{host}:{port}")
    
    res = await client.get("/status")
    assert res == {"ok": True}, f"GET /status failed: {res}"
    
    echo = await client.post("/echo", data={"foo": "bar"})
    assert echo == {"received": {"foo": "bar"}}, f"POST /echo failed: {echo}"
    
    # Cleanup
    server.stop()
    