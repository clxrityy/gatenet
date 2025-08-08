"""
Tests for HTTP base request handler.
"""
import pytest
from unittest.mock import Mock, patch
from io import BytesIO
from http.server import BaseHTTPRequestHandler
from gatenet.http_.base import SimpleHTTPRequestHandler


class TestSimpleHTTPRequestHandler:
    """Test the SimpleHTTPRequestHandler class."""

    def create_mock_handler(self, method='GET', path='/', headers=None):
        """Create a mock handler for testing."""
        if headers is None:
            headers = {}
        
        # Create mock request
        mock_request = Mock()
        mock_request.makefile.return_value = BytesIO()
        
        # Create mock client address
        client_address = ('127.0.0.1', 12345)
        
        # Create mock server
        mock_server = Mock()
        
        # Create handler instance
        handler = SimpleHTTPRequestHandler(mock_request, client_address, mock_server)
        
        # Mock the necessary attributes and methods
        handler.rfile = BytesIO(f"{method} {path} HTTP/1.1\r\n".encode() + 
                               "\r\n".join(f"{k}: {v}" for k, v in headers.items()).encode() + 
                               b"\r\n\r\n")
        handler.wfile = BytesIO()
        handler.command = method
        handler.path = path
        # headers is set by parse_request() normally, we'll mock it differently if needed
        handler.request_version = 'HTTP/1.1'
        
        return handler

    def test_inherits_from_base_http_request_handler(self):
        """Test that SimpleHTTPRequestHandler inherits from BaseHTTPRequestHandler."""
        assert issubclass(SimpleHTTPRequestHandler, BaseHTTPRequestHandler)

    def test_do_get_method_exists(self):
        """Test that do_GET method exists and is callable."""
        assert hasattr(SimpleHTTPRequestHandler, 'do_GET')
        assert callable(getattr(SimpleHTTPRequestHandler, 'do_GET'))

    @patch('gatenet.http_.base.SimpleHTTPRequestHandler.send_response')
    @patch('gatenet.http_.base.SimpleHTTPRequestHandler.send_header')
    @patch('gatenet.http_.base.SimpleHTTPRequestHandler.end_headers')
    def test_do_get_sends_correct_response(self, mock_end_headers, mock_send_header, mock_send_response):
        """Test that do_GET sends the correct HTTP response."""
        handler = self.create_mock_handler()
        
        # Mock wfile write method
        handler.wfile = Mock()
        
        # Call the method
        handler.do_GET()
        
        # Verify response
        mock_send_response.assert_called_once_with(200)
        mock_send_header.assert_called_once_with('Content-type', 'text/plain')
        mock_end_headers.assert_called_once()
        handler.wfile.write.assert_called_once_with(b'Hello from gatenet HTTP server!')

    def test_do_get_response_content(self):
        """Test the actual content of the GET response."""
        handler = self.create_mock_handler()
        
        # Mock the HTTP methods
        with patch.object(handler, 'send_response'), \
             patch.object(handler, 'send_header'), \
             patch.object(handler, 'end_headers'):
            
            # Create a BytesIO object to capture written data
            handler.wfile = BytesIO()
            
            # Call do_GET
            handler.do_GET()
            
            # Check the written content
            written_content = handler.wfile.getvalue()
            assert written_content == b'Hello from gatenet HTTP server!'

    def test_log_message_override(self):
        """Test that log_message is overridden and doesn't output."""
        handler = self.create_mock_handler()
        
        # Test that log_message can be called without error and produces no output
        with patch('sys.stderr') as mock_stderr:
            handler.log_message("Test message %s", "arg")
            # Should not write to stderr
            mock_stderr.write.assert_not_called()

    def test_log_message_with_various_formats(self):
        """Test log_message with different format strings."""
        handler = self.create_mock_handler()
        
        # These should all execute without error or output
        handler.log_message("Simple message")
        handler.log_message("Message with %s", "argument")
        handler.log_message("Message with %s and %d", "string", 42)
        handler.log_message("%s - %s [%s] %s", "127.0.0.1", "-", "timestamp", "GET /")

    def test_handler_initialization(self):
        """Test that handler can be initialized properly."""
        mock_request = Mock()
        mock_request.makefile.return_value = BytesIO()
        client_address = ('127.0.0.1', 12345)
        mock_server = Mock()
        
        # This should not raise an exception
        handler = SimpleHTTPRequestHandler(mock_request, client_address, mock_server)
        assert isinstance(handler, SimpleHTTPRequestHandler)
        assert isinstance(handler, BaseHTTPRequestHandler)

    def test_multiple_get_requests(self):
        """Test handling multiple GET requests."""
        handler = self.create_mock_handler()
        
        responses = []
        
        def capture_write(data):
            responses.append(data)
        
        # Mock the HTTP response methods
        with patch.object(handler, 'send_response'), \
             patch.object(handler, 'send_header'), \
             patch.object(handler, 'end_headers'):
            
            handler.wfile = Mock()
            handler.wfile.write.side_effect = capture_write
            
            # Call do_GET multiple times
            handler.do_GET()
            handler.do_GET()
            handler.do_GET()
            
            # Should have captured 3 identical responses
            assert len(responses) == 3
            assert all(response == b'Hello from gatenet HTTP server!' for response in responses)

    def test_content_type_header(self):
        """Test that the correct content-type header is set."""
        handler = self.create_mock_handler()
        
        with patch.object(handler, 'send_response') as mock_response, \
             patch.object(handler, 'send_header') as mock_header, \
             patch.object(handler, 'end_headers'), \
             patch.object(handler, 'wfile'):
            
            handler.do_GET()
            
            # Verify the content-type header
            mock_header.assert_called_once_with('Content-type', 'text/plain')
            mock_response.assert_called_once_with(200)
