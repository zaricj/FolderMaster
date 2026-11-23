import os
import shutil
from pathlib import Path

from PySide6.QtCore import QObject, Signal

from src.core.rule_config_handler import WILDCARD, RuleConfigHandler, normalize_extensions

# Resolve relative to this file so the app works regardless of the current working directory
CONFIG_FILE = Path(__file__).resolve().parent.parent / "rules" / "rules.json"

# Characters that are not allowed in a single folder name on Windows
_INVALID_FOLDER_CHARS = set('<>:"/\\|?*')


def _scan_files(directory: Path) -> list[os.DirEntry]:
    """Return the regular files of a directory.

    os.scandir caches file-type info from the directory listing, avoiding one extra
    stat() system call per entry compared to Path.iterdir() + is_file().
    """
    with os.scandir(directory) as it:
        return [entry for entry in it if entry.is_file()]


def _matches(filename: str, extensions: set[str]) -> bool:
    return WILDCARD in extensions or Path(filename).suffix.lower() in extensions


def _unique_destination(dest_dir: Path, filename: str) -> Path:
    """Avoid silently overwriting an existing file: 'a.txt' -> 'a (1).txt' -> 'a (2).txt' ..."""
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate
    stem, suffix = Path(filename).stem, Path(filename).suffix
    counter = 1
    while True:
        candidate = dest_dir / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


class AppModel(QObject):
    browse_folder_requested = Signal(str)
    recent_folder_update_requested = Signal(str, int)
    back_button_state_changed = Signal(bool)  # Tells the UI to enable/disable back button
    list_files_requested = Signal(list)  # for list_files method
    load_rules_requested = Signal(dict)  # Load the rule JSON file on startup
    add_to_list_requested = Signal(str, dict)  # Rule name and rule data
    organize_completed = Signal(str, int)

    # Batch table
    remove_row_requested = Signal(int)
    clear_all_rows_requested = Signal()

    error_occurred = Signal(str, str)  # QMessageBox critical (title, message)
    warning_occurred = Signal(str, str)  # QMessageBox warning (title, message)
    info_occurred = Signal(str, str)  # QMessageBox information (title, message)

    append_to_program_output = Signal(str)
    set_text_to_program_output = Signal(str)

    def __init__(self, config_file: str | Path = CONFIG_FILE) -> None:
        super().__init__()
        self.rule_handler = RuleConfigHandler(config_file)
        self.source_folder: str = ""
        self.max_recent_folders = 10
        self._history: list[str] = []  # Navigation stack for the "Go back" button
        self.files: list[str] = []

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def handle_browse_folder_requested(self, path: str) -> None:
        path = os.path.normpath(path) if path else path
        # If they selected the exact same folder they are looking at, do nothing
        if self.source_folder == path:
            return

        # Push the current folder to history (even if it's "")
        # so the user can hit "Back" to return to the startup state
        self._history.append(self.source_folder)
        self.source_folder = path

        self.browse_folder_requested.emit(path)
        self.back_button_state_changed.emit(bool(self._history))

    def handle_recent_folder_update_requested(self, path: str, max_folders: int) -> None:
        self.recent_folder_update_requested.emit(os.path.normpath(path), max_folders)

    def handle_go_back_requested(self) -> None:
        if not self._history:
            return

        self.source_folder = self._history.pop()
        self.browse_folder_requested.emit(self.source_folder)
        self.back_button_state_changed.emit(bool(self._history))

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def _validate_source_dir(self, source_dir: str) -> Path | None:
        """Emit a warning and return None if the directory is unusable."""
        if not source_dir:
            self.warning_occurred.emit(
                "No directory selected",
                "Please select a source folder first.",
            )
            return None

        path = Path(source_dir)
        if not path.is_dir():
            self.warning_occurred.emit(
                "Directory does not exist",
                f"The selected directory does not exist:\n{source_dir}",
            )
            return None
        return path

    @staticmethod
    def _is_valid_folder_name(name: str) -> bool:
        """A target folder must be a single, plain folder name inside the source dir."""
        if not name:
            return True  # Optional
        if name in (".", "..") or name.endswith((" ", ".")):
            return False
        return not any(c in _INVALID_FOLDER_CHARS or ord(c) < 32 for c in name)

    # ------------------------------------------------------------------
    # Rules
    # ------------------------------------------------------------------

    def handle_list_files_requested(self, rule_name: str, source_dir: str) -> None:
        source_path = self._validate_source_dir(source_dir)
        if source_path is None:
            return

        try:
            entries = _scan_files(source_path)
        except OSError as e:
            self.error_occurred.emit("Error", f"Failed to list files: {e}")
            return

        if not rule_name:
            self.set_text_to_program_output.emit(
                "Listing all files in directory as no rule filter has been selected:"
            )
            self.files = sorted((e.name for e in entries), key=str.lower)
        else:
            extensions = set(self.rule_handler.get_custom_rule(rule_name).get("extensions", []))
            self.set_text_to_program_output.emit(f"Files matching rule '{rule_name}':")
            self.files = sorted((e.name for e in entries if _matches(e.name, extensions)), key=str.lower)

        self.list_files_requested.emit(self.files)

    def handle_load_rules_requested(self) -> None:
        self.load_rules_requested.emit(self.rule_handler.data)

    def handle_display_rule_info_requested(self, rule_name: str, source_dir: str) -> None:
        rule = self.rule_handler.get_custom_rule(rule_name) if rule_name else {}
        if not rule:
            self.warning_occurred.emit("No rule selected", "Please select a rule to display its details.")
            return

        extensions = ", ".join(rule.get("extensions", []))
        folder = rule.get("folder") or rule_name
        target = str(Path(source_dir) / folder) if source_dir else f"<source folder>{os.sep}{folder}"

        self.set_text_to_program_output.emit(
            f"Rule Name: {rule_name}\n"
            f"Extensions: {extensions}\n"
            f"Target Folder: {target}"
        )

    def handle_save_rule_requested(self, rule_name: str, opt_folder_name: str, extensions: list) -> None:
        extensions = normalize_extensions(extensions)
        if not rule_name or not extensions:
            self.warning_occurred.emit("Failed to save rule", "The rule name and extensions cannot be empty.")
            return

        if not self._is_valid_folder_name(opt_folder_name):
            self.warning_occurred.emit(
                "Invalid folder name",
                "The optional folder must be a single folder name without any of these "
                'characters: < > : " / \\ | ? *',
            )
            return

        already_exists = rule_name in self.rule_handler.data
        try:
            self.rule_handler.add_custom_rule(rule_name, extensions, opt_folder_name)
        except OSError as e:
            self.error_occurred.emit("Failed to save rule", f"Could not write the rules file:\n{e}")
            return

        if already_exists:
            self.info_occurred.emit(
                "Rule overwritten",
                f"A rule named '{rule_name}' already existed and has been overwritten with the new values.",
            )
        else:
            self.info_occurred.emit("Rule saved", f"Rule '{rule_name}' has been saved successfully!")

        # The handler keeps its in-memory data in sync - no need to re-read the file
        self.load_rules_requested.emit(self.rule_handler.data)

    def handle_add_to_list_requested(self, source_dir: str, rule_name: str) -> None:
        if not rule_name:
            self.warning_occurred.emit("No rule selected", "Please select a rule from the combobox in order to add it to the list.")
            return

        if self._validate_source_dir(source_dir) is None:
            return

        rule_data = self.rule_handler.get_custom_rule(rule_name)
        if not rule_data:
            self.warning_occurred.emit("Rule not found", f"The rule '{rule_name}' could not be found in your configuration.")
            return

        self.add_to_list_requested.emit(rule_name, rule_data)

    # ------------------------------------------------------------------
    # Batch table context menu
    # ------------------------------------------------------------------

    def handle_context_menu_action_requested(self, action: str, current_row: int) -> None:
        if action == "Remove Selected":
            if current_row < 0:
                self.append_to_program_output.emit("No row selected to delete.")
                return
            self.remove_row_requested.emit(current_row)
            self.append_to_program_output.emit(f"Removed item at row: {current_row + 1}")
        elif action == "Remove All":
            self.clear_all_rows_requested.emit()

    # ------------------------------------------------------------------
    # Organize
    # ------------------------------------------------------------------

    def handle_organize_requested(self, batch_rules: list[dict]) -> None:
        """Process every batched rule. Each row carries the source folder it was added for.

        Each source folder is scanned only once; rules are applied in table order and a file
        is moved by the first rule that matches it.
        """
        # Group rows by source folder, keeping table order
        by_source: dict[str, list[dict]] = {}
        for rule in batch_rules:
            by_source.setdefault(rule["source_dir"], []).append(rule)

        errors: list[str] = []
        total_moved = 0

        for source_dir, rules in by_source.items():
            source_path = self._validate_source_dir(source_dir)
            if source_path is None:
                continue

            try:
                remaining = _scan_files(source_path)
            except OSError as e:
                errors.append(f"{source_dir}: {e}")
                continue

            for rule in rules:
                moved, remaining, rule_errors = self._apply_rule(source_path, rule, remaining)
                total_moved += moved
                errors.extend(rule_errors)
                self.organize_completed.emit(rule["rule_name"], moved)

        self.append_to_program_output.emit(f"Done. {total_moved} file(s) moved in total.")

        # Report all failures in one dialog instead of one modal box per file
        if errors:
            shown = "\n".join(errors[:20])
            more = f"\n... and {len(errors) - 20} more." if len(errors) > 20 else ""
            self.error_occurred.emit("Some files could not be moved", f"{shown}{more}")

    def _apply_rule(
        self, source_path: Path, rule: dict, files: list[os.DirEntry]
    ) -> tuple[int, list[os.DirEntry], list[str]]:
        """Move the matching files for a single rule. Returns (moved, unmatched_files, errors)."""
        rule_name: str = rule["rule_name"]
        folder_name: str = rule.get("folder", "").strip() or rule_name

        if not self._is_valid_folder_name(folder_name):
            return 0, files, [f"Rule '{rule_name}': invalid target folder name '{folder_name}'."]

        extensions = set(normalize_extensions(rule.get("extensions", [])))
        matching = [f for f in files if _matches(f.name, extensions)]
        unmatched = [f for f in files if not _matches(f.name, extensions)]

        # Only create the target folder when there is something to move into it
        if not matching:
            return 0, unmatched, []

        dest_path = source_path / folder_name
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return 0, unmatched, [f"Rule '{rule_name}': cannot create '{dest_path}': {e}"]

        moved = 0
        errors: list[str] = []
        for entry in matching:
            try:
                shutil.move(entry.path, _unique_destination(dest_path, entry.name))
                moved += 1
            except OSError as e:
                errors.append(f"{entry.name}: {e}")

        return moved, unmatched, errors
