"""
Example: UDP echo client and server using gatenet
"""
import time
from gatenet.socket.udp import UDPServer
from gatenet.client.udp import UDPClient
from gatenet.utils.net import get_free_port
import threading

def run_server(port):
    server = UDPServer(host="127.0.0.1", port=port)
    server._sock.settimeout(1.0)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    return server, server_thread

def main():
    port = get_free_port()
    server, server_thread = run_server(port)
    time.sleep(0.2)
    try:
        client = UDPClient(host="127.0.0.1", port=port)
        print("Sending: hello")
        response = client.send("hello")
        print("Received:", response)
    finally:
        server.stop()
        server_thread.join(timeout=1)

if __name__ == "__main__":
    main()
