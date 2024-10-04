import os
import tomli
from pathlib import Path
from typing import Dict, Any

# Default paths for configuration
DEFAULT_CONFIG_PATH = Path(__file__).parent / "default_dns_servers.toml"
USER_CONFIG_DIR = Path.home() / ".config" / "dns_changer"
USER_CONFIG_PATH = USER_CONFIG_DIR / "dns_servers.toml"

class Config:
    def __init__(self):
        self.config_path = self._get_config_path()
        self.dns_servers = self._load_config()

    def _get_config_path(self) -> Path:
        """
        Determine which configuration file to use.
        Prioritizes user config, falls back to default if not found.
        """
        if os.environ.get("DNS_CHANGER_CONFIG"):
            return Path(os.environ["DNS_CHANGER_CONFIG"])
        
        if USER_CONFIG_PATH.exists():
            return USER_CONFIG_PATH
        
        # If user config doesn't exist, create it from default
        if not USER_CONFIG_DIR.exists():
            USER_CONFIG_DIR.mkdir(parents=True)
        
        if not USER_CONFIG_PATH.exists():
            DEFAULT_CONFIG_PATH.read_bytes()
            USER_CONFIG_PATH.write_bytes(DEFAULT_CONFIG_PATH.read_bytes())
        
        return USER_CONFIG_PATH

    def _load_config(self) -> Dict[str, Any]:
        """Load and parse the TOML configuration file."""
        try:
            with open(self.config_path, "rb") as f:
                config_data = tomli.load(f)
                return config_data.get("servers", {})
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return {}

    def get_dns_servers(self) -> Dict[str, Dict[str, Any]]:
        """Return the loaded DNS servers configuration."""
        return self.dns_servers

# Create a global config instance
config = Config()
DNS_SERVERS = config.get_dns_servers()
