from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QFileSystemModel, QLineEdit
from PySide6.QtCore import QStandardPaths

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assets.gui.ui.ui_FolderMaster import Ui_MainWindow
    from app import MainWindow

class ComboBoxEvents:
    def __init__(self, ui: "Ui_MainWindow", main_window: "MainWindow"):
        self.ui = ui
        self.main_window = main_window

    def rule_changed(self):
        rule = self.ui.combobox_rules.currentText()

        self.ui.text_edit_program_output.append(
            f"Rule changed to: {rule}"
        )
    
    @Slot()
    def recent_folder_item_changed(self):
        path_to_set = self.ui.combobox_recent_folders.currentText().strip()
        if path_to_set:
            self.ui.line_edit_selected_folder.setText(path_to_set)
            self.update_folder_structure(path_to_set)
            
    def update_folder_structure(self, path: str):
        self.main_window.filesystem_viewer.set_root_path(path)