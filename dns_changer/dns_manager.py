import asyncio
import dns.resolver
from concurrent.futures import ThreadPoolExecutor
import time
from .config import Config
from .network import NetworkManager

class DNSManager:
    def __init__(self):
        self.network_manager = NetworkManager()
        self.config = Config()
        self.dns_servers = self.config.get_dns_servers()

    async def test_dns_speed(self, dns_server, domain):
        """
        Test the response time of a specific DNS server for a given domain.
        
        Args:
            dns_server (str): The IP address of the DNS server to test
            domain (str): The domain name to resolve
            
        Returns:
            float: The response time in seconds, or float('inf') if the test fails
        """
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server]
            resolver.timeout = 2
            resolver.lifetime = 2
            
            start_time = time.time()
            await asyncio.get_event_loop().run_in_executor(
                ThreadPoolExecutor(), resolver.resolve, domain, 'A'
            )
            end_time = time.time()
            return end_time - start_time
        except Exception:
            return float('inf')

    async def find_best_dns(self, domain):
        """
        Find the best DNS servers for a given domain based on response time.
        
        Args:
            domain (str): The domain name to test
            
        Returns:
            list: A list of tuples containing (server_name, ip, speed, rank)
        """
        results = []
        for name, server_info in self.dns_servers.items():
            for ipv4 in server_info['ipv4']:
                speed = await self.test_dns_speed(ipv4, domain)
                if speed != float('inf'):
                    results.append((name, ipv4, speed, server_info['rank']))
        
        results.sort(key=lambda x: (x[2], -x[3]))  # Sort by speed, then by rank (descending)
        return results[:3]  # Return top 3 results

    def change_dns(self, dns_name):
        """
        Change the system DNS to the selected server.
        
        Args:
            dns_name (str): The name of the DNS server from the configuration
            
        Returns:
            tuple: (bool, str) indicating success/failure and a message
        """
        device, conn_type = self.network_manager.get_active_connection()
        if not device:
            return False, "No active connection found"
        
        dns_info = self.dns_servers.get(dns_name)
        if not dns_info:
            return False, f"Invalid DNS server: {dns_name}"
        
        ipv4_dns = ','.join(dns_info['ipv4'])
        ipv6_dns = ','.join(dns_info['ipv6']) if dns_info['ipv6'] else None
        
        if not self.network_manager.change_dns(device, ipv4_dns, ipv6_dns):
            return False, "Failed to change DNS settings"
        
        if not self.network_manager.reset_connection(device, conn_type):
            return False, "Failed to reset network connection"
        
        return True, f"Successfully changed DNS to {dns_name}"
