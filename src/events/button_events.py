from PySide6.QtWidgets import QFileDialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assets.gui.ui.FolderMasterui_ui import Ui_MainWindow
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
            
    def display_rule_info(self, configuration: dict):
        selected_rule = self.ui.combobox_rules.currentText()
        if selected_rule != "Select a rule...":
            ext = configuration[selected_rule]
            extensions = ", ".join(ext)
            # Display in program output
            self.ui.text_edit_program_output.setText(f"Rule '{selected_rule}' has the following extensions:\n{extensions}")

    def save_rule(self):
        pass