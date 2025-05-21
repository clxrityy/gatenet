from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Basic handler that responds to GET requests with a plain text message.
    """
    
    def do_GET(self):
        """Handle GET requests."""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello from gatenet HTTP server!')
        
    def log_message(self, format, *args):
        """Override to prevent logging to stderr."""
        return
        

class HTTPServerComponent:
    """
    Simple HTTP server component.
    
    - Binds to the given host and port.
    - Uses Python's built-in HTTP server.
    - Runs in a background thread via `start()`.
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        """
        Initialize the HTTP server.
        
        :param host: Host address to bind to.
        :param port: Port number to bind to.
        :param handler_cls: Custom request handler class (default is SimpleHTTPRequestHandler).
        """
        from .server import RouteHTTPRequestHandler
        
        self.host = host
        self.port = port
        self.handler_cls = RouteHTTPRequestHandler
        self._server = HTTPServer((self.host, self.port), self.handler_cls)
        self._thread = None
        
    def route(self, path, method: str = "GET"):
        """
        Decorator to register a route handler.
        
        :param path: The path to register the handler for.
        :param method: The HTTP method (GET, POST, etc.).
        """
        def decorator(func):
            self.handler_cls.routes[(path, method.upper())] = func
            return func
        return decorator
        
    def start(self):
        """
        Start the server in a background thread.
        """
        def run():
            try:
                self._server.serve_forever()
            except Exception as e:
                print(f"[HTTP] Server error: {e}")
        
        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()
    
    def stop(self):
        """
        Stop the server.
        """
        if self._server:
            self._server.shutdown()
            self._server.server_close()