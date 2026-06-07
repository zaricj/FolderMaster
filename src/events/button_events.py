from assets.gui.ui.dialogs import info, warning, error
from PySide6.QtWidgets import QFileDialog, QTableWidgetItem, QAbstractItemView
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from assets.gui.ui.ui_FolderMaster import Ui_MainWindow
    from app import MainWindow

class ButtonEvents:
    def __init__(self, ui: "Ui_MainWindow", main_window: "MainWindow", file_manager):
        self.ui = ui
        self.main_window = main_window
        self.file_manager = file_manager

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self.main_window, "Select Directory"
        )

        if folder:
            self.ui.line_edit_selected_folder.setText(folder)
            self.main_window.save_recent_folders(folder)

    def list_files(self):
        rule = self.ui.combobox_rules.currentText()
        source = self.ui.line_edit_selected_folder.text()

        try:
            files = self.file_manager.list_files(source, rule_name=rule)

            self.ui.text_edit_program_output.clear()

            if files:
                header = f"Listing files in '{source}':"
                self.ui.text_edit_program_output.append(header)
                self.ui.text_edit_program_output.append("-" * len(header))

                for i, f in enumerate(files, 1):
                    self.ui.text_edit_program_output.append(f"{i} - {f}")
            else:
                self.ui.text_edit_program_output.setText("No files found.")

        except Exception as e:
            self.ui.text_edit_program_output.setText(f"{type(e).__name__}: {e}")
            
    def display_rule_info(self):
        """Displays details about the selected rule."""
        rule_name = self.ui.combobox_rules.currentText()
        config = self.main_window.config_handler.config
        src_folder = self.ui.line_edit_selected_folder.text()
        
        if rule_name != "Select a rule..." and rule_name in config:
            rule_data = config[rule_name]
            
            # Since extensions are saved as a list, we join them cleanly for display
            extensions = ", ".join(rule_data.get("extensions", []))
            folder = rule_data.get("folder", "None specified")
            target_folder = Path(src_folder) / folder 
            
            output_text = (
                f"Rule Name: {rule_name}\n"
                f"Extensions: {extensions}\n"
                f"Target Folder: {target_folder}"
            )
            self.ui.text_edit_program_output.setText(output_text)

    def save_rule(self):
        rule_name: str = self.ui.line_edit_rule_name.text().strip()
        
        # Split extensions by comma and strip extra whitespaces from each entry
        raw_extensions = self.ui.line_edit_extensions.text()
        extensions: list[str] = [ext.strip() for ext in raw_extensions.split(",") if ext.strip()]
        
        optional_folder_name: str = self.ui.line_edit_opt_folder.text().strip()

        if not rule_name or not extensions:
            self.ui.text_edit_program_output.setText("Error: Rule name and extensions cannot be empty.")
            return

        # Correctly call the updated handler
        self.main_window.config_handler.add_custom_rule(rule_name, extensions, optional_folder_name)
        
        # Give feedback to the user
        self.ui.text_edit_program_output.setText(f"Rule '{rule_name}' successfully saved!")

        # Add the new rule to the combobox
        self.ui.combobox_rules.addItem(rule_name)
        self.main_window.config_handler.load_config()

    def add_rule_to_list(self) -> None:
        """
        Finds the single rule selected in the combobox and appends it 
        as a new row to the batch QTableWidget queue.
        """
        # Get the target rule name from the combobox
        selected_rule = self.ui.combobox_rules.currentText().strip()
        print(f"Selected rule name is: {selected_rule}")
        
        if not selected_rule or selected_rule == "Select a rule...":
            warning(None, "No rule selected", "Please select a rule from the combobox in order to add it to the list.")
            return
    
        table = self.ui.table_widget_batch_rules 
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Keep cells read-only
        
        # Grab your configuration dictionary
        rules_data = self.main_window.config_handler.config
        
        # Look up ONLY the single selected rule
        rule_body = rules_data.get(selected_rule)
        if not rule_body:
            # Fallback safeguard if the combobox text isn't in the config dict
            warning(None, "Rule not found", f"The rule '{selected_rule}' could not be found in your configuration.")
            return
    
        # Optional: Prevent duplicate rows in the batch list
        for row in range(table.rowCount()):
            existing_item = table.item(row, 0)
            if existing_item and existing_item.text() == selected_rule:
                warning(None, "Duplicate Rule", f"The rule '{selected_rule}' is already in your batch list.")
                return
    
        # Extract the data for this specific rule
        extensions_list = rule_body.get("extensions", [])
        folder_name = rule_body.get("folder", "")
        extensions_display = ", ".join(extensions_list)
        
        # Insert exactly ONE new row at the bottom of your table
        row_idx = table.rowCount()
        table.insertRow(row_idx)
        
        # Populate the cells for this rule
        table.setItem(row_idx, 0, QTableWidgetItem(selected_rule))      # Column 0: Rule Name
        table.setItem(row_idx, 1, QTableWidgetItem(extensions_display)) # Column 1: Extensions
        table.setItem(row_idx, 2, QTableWidgetItem(folder_name))        # Column 2: Opt. Folder Name
    
        # Automatically fit column widths cleanly
        table.resizeColumnsToContents()