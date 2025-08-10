import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from typing import Optional
from gatenet.core import Hooks, events
    
class HTTPServerComponent:
    """
    Simple HTTP server component for serving JSON responses.

    - Binds to the given host and port.
    - Uses Python's built-in HTTP server.
    - Runs in a background thread via `start()`.
    - Supports dynamic route registration via the `route` decorator.

    Example
    -------
    >>> from gatenet.http_.server import HTTPServerComponent
    >>> server = HTTPServerComponent(host="127.0.0.1", port=8080)
    >>> @server.route("/status", method="GET")
    ... def status_handler(req):
    ...     return {"ok": True}
    >>> server.start()
    # Now visit http://127.0.0.1:8080/status
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000, hooks: Optional[Hooks] = None):
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
        self.hooks = hooks or Hooks()
        self.server = HTTPServer((self.host, self.port), self._make_handler())

    def _make_handler(self):
        routes = self._routes # Closure to capture routes
        hooks = self.hooks
        
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
                # Before-request hook
                try:
                    hooks.emit(events.HTTP_BEFORE_REQUEST, req=self)
                except Exception:
                    pass

                handler = routes.get((self.path, method))
                if handler:
                    try:
                        result = handler(self)
                        status = 200
                        body = json.dumps(result).encode()
                        self.send_response(status)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(body)
                        # After-response hook
                        try:
                            hooks.emit(
                                events.HTTP_AFTER_RESPONSE,
                                req=self,
                                status=status,
                                headers={"Content-Type": "application/json"},
                                body=body,
                            )
                        except Exception:
                            pass
                    except Exception as e:
                        # Exception hook
                        try:
                            hooks.emit(events.HTTP_EXCEPTION, req=self, exc=e)
                        except Exception:
                            pass
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(b"Internal Server Error \n")
                        self.wfile.write(str(e).encode())
                else:
                    # Route-not-found hook
                    try:
                        hooks.emit(events.HTTP_ROUTE_NOT_FOUND, path=self.path, method=method)
                    except Exception:
                        pass
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