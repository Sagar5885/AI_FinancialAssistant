"""
Configuration loader for AI Finance Assistant
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConfigLoader:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self):
        """Load configuration from YAML file"""
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, 'r') as f:
            self._config = yaml.safe_load(f)
        self._resolve_env_vars()

    def _resolve_env_vars(self):
        """Replace environment variable placeholders"""
        def replace_env(obj):
            if isinstance(obj, dict):
                return {k: replace_env(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_env(item) for item in obj]
            elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
                var_name = obj[2:-1]
                return os.getenv(var_name, obj)
            return obj

        self._config = replace_env(self._config)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration"""
        return self._config


def get_config() -> ConfigLoader:
    """Get configuration singleton"""
    return ConfigLoader()
