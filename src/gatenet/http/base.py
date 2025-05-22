from http.server import BaseHTTPRequestHandler

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
        