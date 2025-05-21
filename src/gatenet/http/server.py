import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

class RouteHTTPRequestHandler(BaseHTTPRequestHandler):
    routes = {}
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        handler = self.routes.get((parsed_path.path, "GET"))
        
        if handler:
            response = handler(self)
            self._send_json(response)
        else:
            self.send_error(404, "Not Found")
            
    def do_POST(self):
        parsed_path = urlparse(self.path)
        handler = self.routes.get((parsed_path.path, "POST"))
        
        if not handler:
            self.send_error(404, "Not Found")
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body) if body else {}
            
        except Exception as e:
            self.send_error(400, f"Invalid JSON: {e}")
            return
        
        response = handler(self, data)
        self._send_json(response)
            
    def _send_json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
            
    def log_message(self, format, *args):
        return # silence logs