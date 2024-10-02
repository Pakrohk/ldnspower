import subprocess
import polycli
from rich.console import Console

console = Console()

class NetworkManager:
    def __init__(self):
        self.cli = polycli.CLI()

    def get_active_connection(self):
        try:
            result = self.cli.run("nmcli -t -f device,type connection show --active")
            if result.success:
                lines = result.output.strip().split('\n')
                if lines:
                    device, conn_type = lines[0].split(':')
                    return device, conn_type
        except Exception as e:
            console.print(f"[red]Error getting active connection: {e}[/red]")
        return None, None

    def reset_connection(self, device, conn_type):
        try:
            # Using polycli to handle elevated privileges
            commands = [
                f"nmcli connection down {device}",
                f"nmcli connection delete {device}",
                f"nmcli connection add type {conn_type} con-name {device} ifname {device}",
                f"nmcli connection up {device}"
            ]
            
            for cmd in commands:
                result = self.cli.run(cmd, sudo=True)
                if not result.success:
                    raise Exception(f"Failed to execute: {cmd}")
            
            return True
        except Exception as e:
            console.print(f"[red]Error resetting network: {e}[/red]")
            return False

    def change_dns(self, device, ipv4_dns, ipv6_dns=None):
        try:
            # Set IPv4 DNS
            result = self.cli.run(f"nmcli connection modify {device} ipv4.dns '{ipv4_dns}'", sudo=True)
            if not result.success:
                raise Exception("Failed to set IPv4 DNS")

            # Handle IPv6 DNS
            if ipv6_dns:
                result = self.cli.run(f"nmcli connection modify {device} ipv6.dns '{ipv6_dns}'", sudo=True)
            else:
                result = self.cli.run(f"nmcli connection modify {device} ipv6.method 'disabled'", sudo=True)
            
            if not result.success:
                raise Exception("Failed to set IPv6 DNS")

            return True
        except Exception as e:
            console.print(f"[red]Error changing DNS: {e}[/red]")
            return False
