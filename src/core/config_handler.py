# config_handler.py
from dataclasses import dataclass
from pathlib import Path
import json
from PySide6.QtWidgets import QMessageBox

# Helper
def create_dir(directory: Path | str):
    if isinstance(directory, str):
        directory = Path(directory)
        
    # Check if it exists
    if not directory.exists():
        Path.mkdir(directory.parent, exist_ok=True)

@dataclass
class Configuration:
    root_dir = Path.cwd()
    config_file = root_dir / "rules" / "rules.json"
    create_dir(config_file)


class ConfigHandler:
    def __init__(self):
        configuration = Configuration()
        self.config_dir = configuration.root_dir
        self.config_file = configuration.config_file
        self.config = self.load_config() # Load the config file

    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                QMessageBox.warning(None, "Warning", f"Warning: {self.config_file} is empty or contains invalid JSON. Using default configuration.")
        return self.get_default_config()

    def get_default_config(self):
        return {"default": {".*"}}

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    # Custom rules
    def add_custom_rule(self, name: str, extensions: list):
        self.config[name] = extensions
        self.save_config()
    
    def get_custom_rule(self, name: str):
        return self.config.get[name, []]
    
    def remove_custom_rule(self, name: str):
        if name in self.config[name]:
            del self.config[name]
            self.save_config()