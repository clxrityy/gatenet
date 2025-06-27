# HTTP Example
# This example demonstrates how to use the HTTP server and client components in Gatenet.

from gatenet.http_.server import HTTPServerComponent
from gatenet.http_.client import HTTPClient
from gatenet.utils.net import get_free_port

# 1. Create the HTTP server
port = get_free_port()
server = HTTPServerComponent(host="127.0.0.1", port=port)


## 1.a Define route methods
@server.route("/ping", method="GET")
def ping_handler(_req):
    return {
        "pong": True
    }

@server.route("/echo", method="POST")
def echo_handler(_req, data):
    return {
        "echo": data
    }

## 1.b Start the server
server.start()

# 2. Create the client
client = HTTPClient(f"http://127.0.0.1:{port}")

## 2.a Make a GET request
res = client.get("/ping")
print("GET /ping ->", res)

## 2.b Make a POST request
payload = {
    "message": "Hello, Gatenet!",
    "count": 1
}
res = client.post("/echo", data=payload)
print("POST /echo ->", res)

# 3. Stop the server
server.stop()