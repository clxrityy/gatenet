"""
Tests for CLI __main__ module entry point.
"""
import pytest
from unittest.mock import patch, MagicMock


class TestCLIMainModule:
    """Test the CLI __main__ module entry point."""

    def test_main_module_execution(self):
        """Test that __main__ module can be imported and contains expected content."""
        # Just test that the module imports correctly and has the main function
        import gatenet.cli.__main__ as main_module
        assert hasattr(main_module, 'main')
        assert callable(main_module.main)

    def test_main_module_import(self):
        """Test that __main__ module can be imported without error."""
        try:
            import gatenet.cli.__main__ as main_module
            # If we get here, import was successful
            assert main_module is not None
        except ImportError as e:
            pytest.fail(f"Failed to import __main__ module: {e}")

    def test_main_function_import(self):
        """Test that main function is properly imported from main module."""
        from gatenet.cli.__main__ import main
        from gatenet.cli.main import main as main_original
        # The imported main should be the same as the original
        assert main == main_original
        assert callable(main)
