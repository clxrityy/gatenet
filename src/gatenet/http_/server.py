import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
    
class HTTPServerComponent:
    """
    Simple HTTP server component for serving JSON responses.

    - Binds to the given host and port.
    - Uses Python's built-in HTTP server.
    - Runs in a background thread via `start()`.
    - Supports dynamic route registration via the `route` decorator.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        """
        Initialize the HTTP server.

        Parameters
        ----------
        host : str, optional
            Host address to bind to (default is "127.0.0.1").
        port : int, optional
            Port number to bind to (default is 8000).
        """
        self.host = host
        self.port = port
        self._routes = {}  # (path, method) -> handler func
        self._thread = None
        self.server = HTTPServer((self.host, self.port), self._make_handler())
    def _make_handler(self):
        routes = self._routes # Closure to capture routes
        
        class RouteHTTPRequestHandler(BaseHTTPRequestHandler):
            routes = {}
            
            def do_GET(self):
                self._handle("GET")
                    
            def do_POST(self):
                self._handle("POST")
                    
            def do_PUT(self):
                self._handle("PUT")
            
            def do_DELETE(self):
                self._handle("DELETE")
            
            def do_PATCH(self):
                self._handle("PATCH")
                
            def _handle(self, method):
                handler = routes.get((self.path, method))
                if handler:
                    try:
                        result = handler(self)
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode())
                    except Exception as e:
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(b"Internal Server Error \n")
                        self.wfile.write(str(e).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(json.dumps({ "code": 404, "error": "Not Found" }).encode())
        return RouteHTTPRequestHandler
        
    def route(self, path: str, method: str = "GET"):
        """
        Decorator to register a route handler.
        
        :param path: The path to register the handler for.
        :param method: The HTTP method (GET, POST, etc.).
        """
        def decorator(func):
            self._routes[(path, method.upper())] = func
            return func
        return decorator
        
    def start(self):
        """
        Start the server in a background thread.
        """
        def run():
            try:
                self.server.serve_forever()
            except Exception as e:
                print(f"[HTTP] Server error: {e}")
        
        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()
    
    def stop(self):
        """
        Stop the server.
        """
        if self.server:
            self.server.shutdown()
            self.server.server_close()