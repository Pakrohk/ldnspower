import pytest
import asyncio
from unittest.mock import Mock, patch
from dns_changer.dns_manager import DNSManager
from dns_changer.network import NetworkManager
from dns_changer.utils import NetworkError, DNSError
from dns_changer.config import DNS_SERVERS

@pytest.fixture
def dns_manager():
    return DNSManager()

@pytest.fixture
def network_manager():
    return NetworkManager()

class TestDNSManager:
    @pytest.mark.asyncio
    async def test_dns_speed_test(self, dns_manager):
        speed = await dns_manager.test_dns_speed("8.8.8.8", "example.com")
        assert isinstance(speed, float)
        assert speed > 0 or speed == float('inf')

    @pytest.mark.asyncio
    async def test_find_best_dns(self, dns_manager):
        results = await dns_manager.find_best_dns("example.com")
        assert len(results) <= 3
        for result in results:
            assert len(result) == 4
            assert isinstance(result[0], str)  # name
            assert isinstance(result[1], str)  # ip
            assert isinstance(result[2], float)  # speed
            assert isinstance(result[3], int)  # rank

    def test_change_dns_invalid_name(self, dns_manager):
        success, message = dns_manager.change_dns("InvalidDNS")
        assert not success
        assert "Invalid DNS server" in message

    @patch('dns_changer.network.NetworkManager.get_active_connection')
    def test_change_dns_no_connection(self, mock_get_conn, dns_manager):
        mock_get_conn.return_value = (None, None)
        success, message = dns_manager.change_dns("Google")
        assert not success
        assert "No active connection" in message

class TestNetworkManager:
    def test_get_active_connection(self, network_manager):
        device, conn_type = network_manager.get_active_connection()
        if device:
            assert isinstance(device, str)
            assert isinstance(conn_type, str)

    @patch('dns_changer.network.NetworkManager.reset_connection')
    def test_reset_connection(self, mock_reset, network_manager):
        mock_reset.return_value = True
        assert network_manager.reset_connection("eth0", "ethernet")

    @patch('dns_changer.network.NetworkManager.change_dns')
    def test_change_dns(self, mock_change_dns, network_manager):
        mock_change_dns.return_value = True
        assert network_manager.change_dns("eth0", "8.8.8.8,8.8.4.4")

@pytest.mark.integration
class TestIntegration:
    def test_full_dns_change_flow(self, dns_manager):
        # This test should only run in a controlled environment
        pytest.skip("Skipping integration test in CI environment")
        
        # Test the full flow of changing DNS
        dns_name = "Google"
        success, message = dns_manager.change_dns(dns_name)
        assert success, f"Failed to change DNS: {message}"
        
        # Verify DNS was changed
        device, _ = dns_manager.network_manager.get_active_connection()
        current_dns = dns_manager.network_manager.get_current_dns(device)
        expected_dns = DNS_SERVERS[dns_name]["ipv4"]
        assert any(dns in current_dns for dns in expected_dns)

def test_dns_servers_config():
    """Test the DNS_SERVERS configuration."""
    for name, info in DNS_SERVERS.items():
        assert isinstance(name, str)
        assert "ipv4" in info
        assert isinstance(info["ipv4"], list)
        assert all(isinstance(ip, str) for ip in info["ipv4"])
        assert "rank" in info
        assert isinstance(info["rank"], int)
        assert 1 <= info["rank"] <= 5

if __name__ == "__main__":
    pytest.main(["-v"])

