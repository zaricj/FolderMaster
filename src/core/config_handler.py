from assets.gui.ui.dialogs import info, warning, error
from dataclasses import dataclass
from pathlib import Path
import json

# Helper
def create_dir_and_file(file_path: Path | str) -> None:
    path = Path(file_path)
    # Ensure the parent directory structure exists
    path.parent.mkdir(parents=True, exist_ok=True)
    # If the file doesn't exist, initialize it as an empty JSON object
    if not path.exists():
        with open(path, "w") as f:
            json.dump({}, f)

@dataclass
class Configuration:
    root_dir: Path = Path().cwd()
    config_file: Path = root_dir / "src" / "rules" / "rules.json"
    
    def __post_init__(self):
        create_dir_and_file(self.config_file)

class ConfigHandler:
    def __init__(self):
        configuration = Configuration()
        self.config_file = configuration.config_file
        self.config = self.load_config() # Load the config file

    def load_config(self) -> dict[str, dict]:
            if self.config_file.exists():
                try:
                    with open(self.config_file, "r") as f:
                        data = json.load(f)
                        # If the JSON file is valid but completely empty ({}),
                        # fall back to default configuration
                        if data:
                            return data
                        return self.get_default_config()
                except json.JSONDecodeError:
                    error(
                        None, 
                        "Warning", 
                        f"Warning: {self.config_file} is corrupted or invalid. Using default configuration."
                    )
                    return self.get_default_config()
            
            # This catches the case where self.config_file.exists() is False
            return self.get_default_config()

    def get_default_config(self) -> dict[str, dict]:
        return {
            "Default": {
                "extensions": [".*"],
                "folder": ""
            }
        }

    def save_config(self) -> None:
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    # Custom rules
    def add_custom_rule(self, name: str, extensions: list[str], folder: str = "") -> None:
        """Adds or updates a rule mapping to your specific JSON format."""
        self.config[name] = {
            "extensions": extensions,
            "folder": folder
        }
        self.save_config()
    
    def get_custom_rule(self, name: str) -> dict | None:
        """Returns the dictionary containing extensions and folder, or None if not found."""
        return self.config.get(name)
    
    def remove_custom_rule(self, name: str) -> None:
        """Safely removes a rule by its name."""
        if name in self.config:
            del self.config[name]
            self.save_config()