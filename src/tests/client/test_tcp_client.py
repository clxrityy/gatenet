import threading
import time
from gatenet.socket import TCPServer
from gatenet.client import TCPClient

def test_tcp_client_echo():
    server = TCPServer("127.0.0.1", 9200)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    
    time.sleep(0.5) # Give the server time to start

    client = TCPClient("127.0.0.1", 9200)
    client.connect()
    
    response = client.send("hello tcp")
    client.close()
    server.stop()
    
    assert response == "Echo: hello tcp"