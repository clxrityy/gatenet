"""
Example: HTTP server with custom routes using gatenet
"""
import time
from gatenet.http_.server import HTTPServerComponent
from gatenet.http_.client import HTTPClient
from gatenet.utils.net import get_free_port
import threading

def main():
    port = get_free_port()
    server = HTTPServerComponent(host="127.0.0.1", port=port)

    @server.route("/status", method="GET")
    def status_handler(req):
        return {"ok": True}

    @server.route("/echo", method="POST")
    def echo_handler(req):
        return {"echo": req.json}

    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    time.sleep(0.2)
    try:
        client = HTTPClient(f"http://127.0.0.1:{port}")
        # Use getattr to call dynamically attached methods for static analysis compatibility
        get = getattr(client, "get")
        post = getattr(client, "post")
        print("GET /status:", get("/status")["data"])
        print("POST /echo:", post("/echo", data={"msg": "hello"})["data"])
    finally:
        server.stop()
        server_thread.join(timeout=1)

if __name__ == "__main__":
    main()
