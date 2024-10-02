import asyncio
import dns.resolver
from concurrent.futures import ThreadPoolExecutor
import time
from .config import DNS_SERVERS
from .network import NetworkManager

class DNSManager:
    def __init__(self):
        self.network_manager = NetworkManager()

    async def test_dns_speed(self, dns_server, domain):
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
        results = []
        for name, servers in DNS_SERVERS.items():
            for ipv4 in servers['ipv4']:
                speed = await self.test_dns_speed(ipv4, domain)
                if speed != float('inf'):
                    results.append((name, ipv4, speed, servers['rank']))
        
        results.sort(key=lambda x: (x[2], -x[3]))
        return results[:3]

    def change_dns(self, dns_name):
        device, conn_type = self.network_manager.get_active_connection()
        if not device:
            return False, "No active connection found"
        
        dns_info = DNS_SERVERS.get(dns_name)
        if not dns_info:
            return False, f"Invalid DNS server: {dns_name}"
        
        ipv4_dns = ','.join(dns_info['ipv4'])
        ipv6_dns = ','.join(dns_info['ipv6']) if dns_info['ipv6'] else None
        
        if not self.network_manager.change_dns(device, ipv4_dns, ipv6_dns):
            return False, "Failed to change DNS settings"
        
        if not self.network_manager.reset_connection(device, conn_type):
            return False, "Failed to reset network connection"
        
        return True, f"Successfully changed DNS to {dns_name}"
