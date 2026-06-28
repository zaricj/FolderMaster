from pathlib import Path
from PySide6.QtCore import QObject, Signal, QPoint
from src.core.rule_config_handler import RuleConfigHandler


CONFIG_FILE = Path().cwd() / "src" / "rules" / "rules.json"

class AppModel(QObject):
    browse_folder_requested = Signal(str)
    recent_folder_update_requested = Signal(str, int)
    back_button_state_changed = Signal(bool)  # Tells the UI to enable/disable back button
    list_files_requested = Signal(list)  # for list_files method
    load_rules_requested = Signal(dict)  # Load the rule JSON file on startup
    add_to_list_requested = Signal(str, dict) # Rule name and rule data
    organize_completed = Signal(str, int)
    
    # Context menu
    show_context_menu_requested = Signal(QPoint)
    context_menu_action_requested = Signal(str)
    remove_row_requested = Signal(int)
    clear_all_rows_requested = Signal()

    error_occurred = Signal(str, str)  # QMessageBox critical (title, message)
    warning_occurred = Signal(str, str)  # QMessageBox warning (title, message)
    info_occurred = Signal(str, str)  # QMessageBox information (title, message)

    append_to_program_output = Signal(str)
    set_text_to_program_output = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.rule_handler = RuleConfigHandler(CONFIG_FILE)
        self.source_folder: str = ""
        self.max_recent_folders = 10
        self._history: list[str] = []  # Clear tracking stack for paths
        self.files: list[str] = []


    def handle_browse_folder_requested(self, path: str) -> None:
        if self.source_folder != path:
            # Before overriding our current folder, push it to history stack
            if self.source_folder:
                self._history.append(self.source_folder)
                self.back_button_state_changed.emit(True)

            self.source_folder = path
            self.browse_folder_requested.emit(path)


    def handle_recent_folder_update_requested(self, path: str, max_folders: int) -> None:
        # (Your existing logic is fine here)
        self.recent_folder_update_requested.emit(path, max_folders)


    def handle_go_back_requested(self):
        if not self._history:
            return

        # Pop the last folder off the stack and make it active
        previous_path = self._history.pop()
        self.source_folder = previous_path

        # Broadcast the changes back out to the app architecture
        self.browse_folder_requested.emit(previous_path)
        self.back_button_state_changed.emit(len(self._history) > 0)


    def handle_list_files_requested(self, rule_name: str, source_dir: str) -> None:
        try:
            if source_dir == "":
                self.warning_occurred.emit(
                    "No directory selected",
                    "Please select a directory from which you want to list files.",
                )
                return

            if not Path(source_dir).exists():
                self.warning_occurred.emit(
                    "Directory does not exist", "The selected directory does not exist."
                )
                return

            if rule_name == "Select a rule...":
                self.append_to_program_output.emit(
                    "Listing all files in directory as no rule filter has been selected:"
                )
                self.files = [
                    file.name for file in Path(source_dir).iterdir() if file.is_file()
                ]
                self.list_files_requested.emit(self.files)

            else:
                rule_data = self.rule_handler.get_custom_rule(rule_name)
                extensions = [ext.lower() for ext in rule_data.get("extensions", [])]

                self.files = [
                    file.name
                    for file in Path(source_dir).iterdir()
                    if file.is_file() and file.suffix.lower() in extensions
                ]

                self.list_files_requested.emit(self.files)

        except Exception as e:
            self.error_occurred.emit("Error", f"Failed to list files: {e}")
            return []


    def handle_load_rules_requested(self) -> None:
        rules_data = self.rule_handler.data
        self.load_rules_requested.emit(rules_data)


    def handle_display_rule_info_requested(self, rule_name: str, source_dir: str) -> None:
        if rule_name != "Select a rule..." and rule_name in self.rule_handler.data:
            selected_rule_data = self.rule_handler.data[rule_name]
            
            # Since extensions are saved as a list, we join them cleanly for display
            extensions = ", ".join(selected_rule_data.get("extensions", []))
            folder = selected_rule_data.get("folder", "None specified")
            target_folder = Path(source_dir) / folder 
            
            output_text = (
                f"Rule Name: {rule_name}\n"
                f"Extensions: {extensions}\n"
                f"Target Folder: {target_folder}"
            )
            self.set_text_to_program_output.emit(output_text)


    def handle_save_rule_requested(self, rule_name: str, opt_folder_name: str, extensions: list) -> None:
        if not rule_name or not extensions:
            self.warning_occurred.emit("Failed to save rule", "The Rule name and extensions cannot be empty.")
            return

        # Check the handler dictionary for same rule names
        current_rules = self.rule_handler.data
        
        if rule_name in current_rules:
            self.rule_handler.add_custom_rule(rule_name, extensions, opt_folder_name)
            self.info_occurred.emit("Rule overwritten", f"A rule named '{rule_name}' already exists.\nThe rule has been overwritten with new values!")
            # Reload the rule configuration file 
            new_rule_data = self.rule_handler.load_config()
            self.load_rules_requested.emit(new_rule_data)
        
        else:
            self.rule_handler.add_custom_rule(rule_name, extensions, opt_folder_name)
            self.info_occurred.emit("Rule saved", f"Rule '{rule_name}' has been saved successfully!")
            # Reload the rule configuration file 
            new_rule_data = self.rule_handler.load_config()
            self.load_rules_requested.emit(new_rule_data)


    def handle_add_to_list_requested(self, source_dir: str, rule_name: str) -> None:
        if rule_name == "Select a rule...":
            self.warning_occurred.emit("No rule selected", "Please select a rule from the combobox in order to add it to the list.")
            return
        
        if source_dir == "":
            self.warning_occurred.emit(
                "No directory selected",
                "Source directory cannot be empty, please select a source folder."
            )
            return
        
        # Look up only the single selected rule from the combobox
        rule_data = self.rule_handler.data[rule_name]
        
        if not rule_data:
            self.warning_occurred.emit("Rule not found", f"The rule '{rule_name}' could not be found in your configuration.")
            return
        else:
            self.add_to_list_requested.emit(rule_name, rule_data)


    def handle_context_menu_action_requested(self, action: str, current_row: int) -> None:
        if action == "Remove Selected":
            self.remove_selected_row(current_row)
        elif action == "Remove All":
            self.remove_all_selected_rows()


    def remove_selected_row(self, current_row: int) -> None:
        try:
            if current_row != -1:
                self.remove_row_requested.emit(current_row)
                self.append_to_program_output.emit(f"Removed item at row: {current_row}")
            else:
                self.append_to_program_output.emit("No row selected to delete.")
        except Exception as ex:
            message = f"An exception of type {type(ex).__name__} occurred. Arguments: {ex.args!r}"
            self.set_text_to_program_output.emit(f"Error removing selected item from table: {message}")


    def remove_all_selected_rows(self) -> None:
        try:
            # We don't check row count here; we let the View handle its own structural reset
            self.clear_all_rows_requested.emit()
        except Exception as ex:
            message = f"An exception of type {type(ex).__name__} occurred. Arguments: {ex.args!r}"
            self.set_text_to_program_output.emit(f"Error removing all rows from table: {message}")


    def handle_organize_requested(self, source_dir: str, batch_rules: list[dict]) -> None:
        """Iterates through every batched rule and processes file sorting."""
        if not source_dir:
            self.warning_occurred.emit("No directory selected", "The source directory cannot be empty.")
            return

        source_path: Path = Path(source_dir)
        
        if not source_path.exists():
            self.warning_occurred.emit("Warning", "Source folder does not exist.")
            return

        for rule in batch_rules:  # ◄── 'rule' is the single item dictionary
            rule_name: str = rule["rule_name"]
            opt_folder_name: str = rule["folder"].strip()
            
            if opt_folder_name:
                dest_path: Path = source_path / opt_folder_name
            else:
                dest_path: Path = source_path / rule_name

            if not dest_path.exists():
                dest_path.mkdir(parents=True, exist_ok=True)
    
            self.execute_file_organization(source_path, dest_path, rule)


    def execute_file_organization(self, source_path: Path, dest_path: Path, rule_config: dict) -> None:
        """Executes actual file adjustments based on selected extensions criteria."""
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
            extensions = rule_config.get("extensions", [])
            
            # Strip out leading asterisks '*' so '*.txt' becomes '.txt' for example
            extensions_lower = [ext.lower().lstrip('*') for ext in extensions]
            moved_count = 0

            for file in source_path.iterdir():
                if file.is_file() and file.suffix.lower() in extensions_lower:
                    dst_file = dest_path / file.name
                    try:
                        from shutil import move
                        move(str(file), str(dst_file))
                        moved_count += 1
                    except Exception as e:
                        self.error_occurred.emit("Error", f"Failed to move file '{file.name}': {e}")

            # FIX: Corrected variable name referencing 'rule_config' here
            self.organize_completed.emit(rule_config["rule_name"], moved_count)

        except Exception as e:
            self.error_occurred.emit("Error", f"Failed to organize batch: {e}")