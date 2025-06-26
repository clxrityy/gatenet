import time
from gatenet.http_ import HTTPServerComponent, HTTPClient
from gatenet.utils import get_free_port
import json



def test_http_client_basic_get_and_post():
    host = "127.0.0.1"
    port = get_free_port()
    server = HTTPServerComponent(host=host, port=port)

    # Test GET
    @server.route("/status", method="GET")
    def status_handler(req):
        return {"ok": True}

    # Test POST
    @server.route("/echo", method="POST")
    def echo_handler(req):
        try:
            length = int(req.headers.get('Content-Length', 0))
            body = req.rfile.read(length)
            data = json.loads(body)
            return {"received": data}
        except Exception as e:
            return {"error": str(e)}, 500

    server.start()
    time.sleep(0.5)

    client = HTTPClient(f"http://{host}:{port}")

    # Test GET
    res = client.get("/status")
    assert {"ok": True} == res["data"]

    # Test POST with JSON body
    echo = client.post("/echo", {"foo": "bar"})
    assert {"received": {"foo": "bar"}} == echo["data"]

    server.stop()

