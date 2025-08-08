"""
Tests for client base module.
"""
import pytest
from abc import ABC
from gatenet.client.base import BaseClient


class TestBaseClient:
    """Test the BaseClient abstract base class."""

    def test_base_client_is_abstract(self):
        """Test that BaseClient cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            BaseClient() # pyright: ignore[reportAbstractUsage]

    def test_base_client_is_abc(self):
        """Test that BaseClient inherits from ABC."""
        assert issubclass(BaseClient, ABC)

    def test_abstract_methods_exist(self):
        """Test that required abstract methods are defined."""
        abstract_methods = BaseClient.__abstractmethods__
        assert 'send' in abstract_methods
        assert 'close' in abstract_methods

    def test_concrete_implementation_works(self):
        """Test that a concrete implementation can be instantiated and used."""
        class ConcreteClient(BaseClient):
            def __init__(self):
                self.closed = False
                self.sent_messages = []

            def send(self, message: str, **kwargs) -> str:
                if self.closed:
                    raise ConnectionError("Client is closed")
                self.sent_messages.append(message)
                return f"response to {message}"

            def close(self):
                self.closed = True

        client = ConcreteClient()
        assert isinstance(client, BaseClient)
        
        # Test send method
        response = client.send("test message")
        assert response == "response to test message"
        assert "test message" in client.sent_messages

        # Test close method
        client.close()
        assert client.closed

        # Test send after close raises error
        with pytest.raises(ConnectionError, match="Client is closed"):
            client.send("another message")

    def test_incomplete_implementation_fails(self):
        """Test that incomplete implementations cannot be instantiated."""
        # Missing close method
        class IncompleteClient1(BaseClient):
            def send(self, message: str, **kwargs) -> str:
                return "response"

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteClient1() # pyright: ignore[reportAbstractUsage]

        # Missing send method
        class IncompleteClient2(BaseClient):
            def close(self):
                # This method is intentionally empty for testing abstract class requirements
                pass

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteClient2() # pyright: ignore[reportAbstractUsage]

    def test_send_with_kwargs(self):
        """Test that send method can accept keyword arguments."""
        class KwargsClient(BaseClient):
            def send(self, message: str, **kwargs) -> str:
                timeout = kwargs.get('timeout', 5)
                host = kwargs.get('host', 'localhost')
                return f"{message} to {host} with timeout {timeout}"

            def close(self):
                # Test implementation - no actual resources to close
                pass

        client = KwargsClient()
        response = client.send("hello", timeout=10, host="example.com")
        assert "hello to example.com with timeout 10" == response

    def test_multiple_inheritance(self):
        """Test that BaseClient works with multiple inheritance."""
        class Loggable:
            def __init__(self):
                self.logs = []

            def log(self, message: str):
                self.logs.append(message)

        class LoggingClient(BaseClient, Loggable):
            def __init__(self):
                super().__init__()

            def send(self, message: str, **kwargs) -> str:
                self.log(f"Sending: {message}")
                return f"Sent: {message}"

            def close(self):
                # Test implementation for logging
                self.log("Closing connection")

        client = LoggingClient()
        client.send("test")
        client.close()
        
        assert "Sending: test" in client.logs
        assert "Closing connection" in client.logs
