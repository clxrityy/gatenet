from http.server import BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Basic HTTP request handler that responds to GET requests with a plain text message.
    """

    def do_GET(self):
        """
        Handle HTTP GET requests.

        Sends a 200 OK response with a plain text message body.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello from gatenet HTTP server!')

    def log_message(self, format, *args):
        """
        Override to prevent logging to stderr.

        Parameters
        ----------
        format : str
            The format string for the log message.
        *args : tuple
            Arguments for the format string.
        """
        pass
