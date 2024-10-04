import os
import typer
import asyncio
from rich.console import Console
from rich.table import Table
from pathlib import Path
from typing import Optional
from .config import Config
from .dns_manager import DNSManager

app = typer.Typer()
console = Console()
config = Config()
dns_manager = DNSManager()

def show_dns_table():
    """Display a table of available DNS servers."""
    table = Table(title="Available DNS Servers")
    table.add_column("Number", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("IPv4", style="green")
    table.add_column("IPv6", style="yellow")
    table.add_column("Rank", style="red")

    dns_servers = config.get_dns_servers()
    for i, (name, info) in enumerate(dns_servers.items(), 1):
        ipv4 = ', '.join(info['ipv4'])
        ipv6 = ', '.join(info['ipv6']) if info['ipv6'] else "Disabled"
        rank_display = "⭐" * info['rank']
        table.add_row(str(i), name, ipv4, ipv6, rank_display)

    console.print(table)

def show_best_dns_table(results, domain):
    """Display a table of the best DNS servers for a given domain."""
    if results:
        table = Table(title=f"Best DNS Servers for {domain}")
        table.add_column("Rank", style="cyan")
        table.add_column("DNS Provider", style="magenta")
        table.add_column("IP", style="green")
        table.add_column("Response Time", style="yellow")
        
        for i, (name, ip, speed, rank) in enumerate(results, 1):
            table.add_row(str(i), name, ip, f"{speed:.3f}s")
        
        console.print(table)

@app.command()
def main(
    domain: Optional[str] = typer.Option(None, "--domain", "-d", help="Domain to test DNS speeds"),
    config_path: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to custom config file"
    ),
    show_config: bool = typer.Option(
        False,
        "--show-config",
        help="Show the current config file path and exit"
    )
):
    """
    Enhanced DNS Changer - Easily change and test DNS servers
    """
    console.print("[bold blue]Enhanced DNS Changer[/bold blue]")
    
    # Initialize config and DNS manager
    if config_path:
        os.environ["DNS_CHANGER_CONFIG"] = str(config_path)
    
    config = Config()
    dns_manager = DNSManager()
    
    if show_config:
        console.print(f"Current config file: {config.config_path}")
        return
    
    # Show current configuration file location
    console.print(f"Using configuration file: {config.config_path}")
    console.print("You can edit this file to add or modify DNS servers.")
    
    # Test DNS speeds if domain is provided
    if domain:
        console.print(f"[yellow]Testing DNS speeds for domain: {domain}[/yellow]")
        results = asyncio.run(dns_manager.find_best_dns(domain))
        show_best_dns_table(results, domain)
    
    # Show available DNS servers
    show_dns_table()
    
    # Get user choice
    dns_servers = config.get_dns_servers()
    if not dns_servers:
        console.print("[red]No DNS servers found in configuration![/red]")
        raise typer.Exit(1)
    
    dns_choice = typer.prompt("Enter the number of your desired DNS", type=int)
    
    if 1 <= dns_choice <= len(dns_servers):
        dns_name = list(dns_servers.keys())[dns_choice - 1]
        success, message = dns_manager.change_dns(dns_name)
        if success:
            console.print(f"[green]{message}[/green]")
        else:
            console.print(f"[red]{message}[/red]")
    else:
        console.print("[red]Invalid choice![/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
