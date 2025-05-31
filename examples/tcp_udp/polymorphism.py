from gatenet.client.tcp import TCPClient
from gatenet.client.udp import UDPClient
from gatenet.client.base import BaseClient

def use_client(client: BaseClient):
    with client:
        response = client.send("hello server")
        print(f"Response: {response}")
        
# You can now swap protocols dynamically
use_client(TCPClient("127.0.0.1", 9000))
use_client(UDPClient("127.0.0.1", 9001))