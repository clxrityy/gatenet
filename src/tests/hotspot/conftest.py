"""
Hotspot-specific test configuration to prevent password prompts.
"""
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def mock_subprocess_for_hotspot():
    """Automatically mock subprocess calls for hotspot tests to prevent password prompts."""
    def _mock_subprocess_success(*args, **kwargs):
        """Mock subprocess calls to return success without prompting for passwords."""
        return MagicMock(returncode=0, stdout="", stderr="")
    
    with patch('subprocess.run', side_effect=_mock_subprocess_success):
        with patch('subprocess.Popen') as mock_popen:
            mock_process = MagicMock()
            mock_process.communicate.return_value = ("", "")
            mock_process.returncode = 0
            mock_popen.return_value = mock_process
            yield
