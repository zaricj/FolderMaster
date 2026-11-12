"""Persistence layer for the user-defined sorting rules (rules.json)."""

import json
import logging
import os
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

WILDCARD = ".*"  # Matches every file regardless of its extension


def normalize_extension(ext: str) -> str:
    """Normalise user input like 'TXT', '*.txt' or ' .Txt ' to '.txt'."""
    ext = ext.strip().lower()
    if ext in ("*", ".*", "*.*"):
        return WILDCARD
    ext = ext.lstrip("*").strip()
    if not ext:
        return ""
    return ext if ext.startswith(".") else f".{ext}"


def normalize_extensions(extensions: list[str]) -> list[str]:
    """Normalise and de-duplicate a list of extensions, preserving order."""
    return list(dict.fromkeys(e for e in map(normalize_extension, extensions) if e))


class RuleConfigHandler:
    def __init__(self, config_file: str | Path) -> None:
        self.config_file = Path(config_file)
        self.data: dict[str, dict] = self.load_config()

    def load_config(self) -> dict[str, dict]:
        try:
            with self.config_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return self.get_default_config()
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("%s is unreadable or invalid (%s). Using default configuration.", self.config_file, e)
            return self.get_default_config()

        # A valid file that is empty ({}) or not a mapping falls back to the defaults
        if not isinstance(data, dict) or not data:
            return self.get_default_config()
        return data

    @staticmethod
    def get_default_config() -> dict[str, dict]:
        return {"Default": {"extensions": [".*"], "folder": ""}}

    def save_config(self) -> None:
        """Write atomically so a crash mid-write can never corrupt rules.json."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=self.config_file.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            os.replace(tmp_path, self.config_file)
        except BaseException:
            Path(tmp_path).unlink(missing_ok=True)
            raise

    # Custom rules
    def add_custom_rule(self, name: str, extensions: list[str], folder: str = "") -> None:
        """Adds or updates a rule. Raises OSError if the file cannot be written."""
        self.data[name] = {"extensions": normalize_extensions(extensions), "folder": folder}
        self.save_config()

    def get_custom_rule(self, name: str) -> dict:
        """Returns the dict containing extensions and folder, or {} if not found."""
        return self.data.get(name, {})

    def remove_custom_rule(self, name: str) -> None:
        """Safely removes a rule by its name."""
        if name in self.data:
            del self.data[name]
            self.save_config()
