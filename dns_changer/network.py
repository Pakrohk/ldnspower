import subprocess
from rich.console import Console

console = Console()

class NetworkManager:
    def __init__(self):
        pass

    def run_command(self, command, sudo=False):
        try:
            if sudo:
                command = f"sudo {command}"
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                raise Exception(result.stderr.strip())
        except Exception as e:
            console.print(f"[red]Error running command: {e}[/red]")
            return False, None

    def get_active_connection(self):
        success, output = self.run_command("nmcli -t -f device,type connection show --active")
        if success:
            lines = output.split('\n')
            if lines:
                device, conn_type = lines[0].split(':')
                return device, conn_type
        return None, None

    def reset_connection(self, device, conn_type):
        commands = [
            f"nmcli connection down {device}",
            f"nmcli connection delete {device}",
            f"nmcli connection add type {conn_type} con-name {device} ifname {device}",
            f"nmcli connection up {device}"
        ]
        
        for cmd in commands:
            success, _ = self.run_command(cmd, sudo=True)
            if not success:
                console.print(f"[red]Failed to execute: {cmd}[/red]")
                return False
            
        return True

    def change_dns(self, device, ipv4_dns, ipv6_dns=None):
        success, _ = self.run_command(f"nmcli connection modify {device} ipv4.dns '{ipv4_dns}'", sudo=True)
        if not success:
            return False

        if ipv6_dns:
            success, _ = self.run_command(f"nmcli connection modify {device} ipv6.dns '{ipv6_dns}'", sudo=True)
        else:
            success, _ = self.run_command(f"nmcli connection modify {device} ipv6.method 'disabled'", sudo=True)
        
        return success

