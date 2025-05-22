import time
import requests
from gatenet.http.base import HTTPServerComponent
from gatenet.utils.net import get_free_port

    
def test_custom_route_json():
    port = get_free_port()
    server = HTTPServerComponent("127.0.0.1", port)
    
    @server.route("/")
    def root(_):
        return {
            "ok": True
        }
    
    @server.route("/ping")
    def ping(_):
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
    def echo(_req, data):
        return {
            "you_sent": data
        }
    
    server.start()
    time.sleep(0.5) # Give the server a moment to start
    
    payload = { "messsage": "hello", "count": 3}
    res = requests.post(f"http://{host}:{port}/echo", json=payload)
    
    assert res.status_code == 200
    assert res.json() == { "you_sent": payload }
    
    server.stop()