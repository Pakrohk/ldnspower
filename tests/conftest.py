
import pytest
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )

@pytest.fixture(scope="session", autouse=True)
def cleanup_after_tests():
    """Cleanup after all tests have run."""
    yield
    # Any cleanup code here if needed

@pytest.fixture
def mock_dns_response():
    """Mock DNS response for testing."""
    return {
        "Google": {"response_time": 0.1},
        "Cloudflare": {"response_time": 0.15},
        "OpenDNS": {"response_time": 0.2},
    }
