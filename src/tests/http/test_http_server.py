import time
import requests
from gatenet.http import HTTPServerComponent
from gatenet.utils import get_free_port
import json

    
def test_custom_route_json():
    port = get_free_port()
    server = HTTPServerComponent("127.0.0.1", port)
    
    @server.route("/")
    def root(req):
        return {
            "ok": True
        }
    
    @server.route("/ping")
    def ping(req):
        return {
            "pong": True
        }
    
    server.start()
    
    time.sleep(0.3) # Give the server a moment to start
    
    r = requests.get(f"http://127.0.0.1:{port}", timeout=2)
    
    assert r.status_code == 200
    assert r.json() == {"ok": True}

    server.stop()
    
def test_http_post_json_echo():
    host = "127.0.0.1"
    port = get_free_port()
    
    server = HTTPServerComponent(host, port)
    
    @server.route("/echo", method="POST")
    def echo(req):
        length = int(req.headers.get('Content-Length', 0))
        body = req.rfile.read(length)
        data = json.loads(body)
        return { "you_sent": data }
    
    server.start()
    time.sleep(0.5) # Give the server a moment to start
    
    payload = { "messsage": "hello", "count": 3}
    res = requests.post(f"http://{host}:{port}/echo", json=payload)
    
    assert res.status_code == 200
    assert res.json() == { "you_sent": payload }
    
    server.stop()