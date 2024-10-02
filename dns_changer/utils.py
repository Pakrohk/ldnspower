import socket
import logging
from rich.logging import RichHandler
from typing import Tuple, Optional, List

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("dns_changer")

def is_valid_ip(ip: str) -> bool:
    """Check if the given string is a valid IP address."""
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return True
        except socket.error:
            return False

def parse_dns_string(dns_string: str) -> List[str]:
    """Parse a comma-separated DNS string into a list of IPs."""
    dns_list = [ip.strip() for ip in dns_string.split(',')]
    return [ip for ip in dns_list if is_valid_ip(ip)]

def format_dns_for_display(dns_list: List[str]) -> str:
    """Format a list of DNS IPs for display."""
    return ', '.join(dns_list)

def get_current_dns() -> Tuple[Optional[List[str]], Optional[List[str]]]:
    """Get current system DNS settings."""
    ipv4_dns = []
    ipv6_dns = []
    
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if line.startswith('nameserver'):
                    ip = line.split()[1]
                    if is_valid_ip(ip):
                        if ':' in ip:
                            ipv6_dns.append(ip)
                        else:
                            ipv4_dns.append(ip)
    except Exception as e:
        logger.error(f"Error reading current DNS settings: {e}")
        return None, None
    
    return ipv4_dns, ipv6_dns

def calculate_dns_rank(speed: float, reliability: float) -> int:
    """Calculate a DNS rank based on speed and reliability."""
    if speed == float('inf') or reliability == 0:
        return 0
    
    score = (1 / speed) * reliability * 5
    return max(1, min(5, round(score)))

class NetworkError(Exception):
    """Custom exception for network-related errors."""
    pass

class DNSError(Exception):
    """Custom exception for DNS-related errors."""
    pass

def safe_run_command(cmd: str) -> Tuple[bool, str]:
    """Safely run a system command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                               capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        return False, str(e)
    except Exception as e:
        logger.error(f"Unexpected error running command: {e}")
        return False, str(e)
