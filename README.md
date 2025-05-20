# gatenet

##### BETA (0.0.1)

## Installation

```zsh
pip install gatenet
```

## Usage

### TCPServer

```py
from gatenet.socket.tcp import TCPServer

server = TCPServer(host='127.0.0.1', port=9090)
server.start()
```

#### With threading
```py
import threading
from gatenet.socket.tcp import TCPServer

tcp_server = TCPServer(host='0.0.0.0', port=8000)
thread = threading.Thread(target=tcp_server.start, daemon=True)
thread.start()
```