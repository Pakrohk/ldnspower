import typer
import asyncio
from rich.console import Console
from rich.table import Table
from .config import DNS_SERVERS
from .dns_manager import DNSManager

app = typer.Typer()
console = Console()
dns_manager = DNSManager()

def show_dns_table():
    table = Table(title="Available DNS Servers")
    table.add_column("Number", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("IPv4", style="green")
    table.add_column("IPv6", style="yellow")
    table.add_column("Rank", style="red")

    for i, (name, info) in enumerate(DNS_SERVERS.items(), 1):
        ipv4 = ', '.join(info['ipv4'])
        ipv6 = ', '.join(info['ipv6']) if info['ipv6'] else "Disabled"
        rank_display = "⭐" * info['rank']
        table.add_row(str(i), name, ipv4, ipv6, rank_display)

    console.print(table)

def show_best_dns_table(results, domain):
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
def main(domain: str = typer.Option(None, "--domain", "-d", help="Domain to test DNS speeds")):
    """
    Enhanced DNS Changer - Easily change and test DNS servers
    """
    console.print("[bold blue]Enhanced DNS Changer[/bold blue]")
    
    if domain:
        console.print(f"[yellow]Testing DNS speeds for domain: {domain}[/yellow]")
        results = asyncio.run(dns_manager.find_best_dns(domain))
        show_best_dns_table(results, domain)
    
    show_dns_table()
    
    dns_choice = typer.prompt("Enter the number of your desired DNS", type=int)
    
    if 1 <= dns_choice <= len(DNS_SERVERS):
        dns_name = list(DNS_SERVERS.keys())[dns_choice - 1]
        success, message = dns_manager.change_dns(dns_name)
        if success:
            console.print(f"[green]{message}[/green]")
        else:
            console.print(f"[red]{message}[/red]")
    else:
        console.print("[red]Invalid choice![/red]")

if __name__ == "__main__":
    app.run()
