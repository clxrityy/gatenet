import threading
import time
from gatenet.socket import UDPServer
from gatenet.client import UDPClient

def test_udp_client_echo():
    server = UDPServer("127.0.0.1", 9300)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    
    time.sleep(0.5)  # Give the server time to start
    
    client = UDPClient("127.0.0.1", 9300)
    response = client.send("hello udp")
    client.close()
    server.stop()
    
    assert response == "Echo: hello udp"