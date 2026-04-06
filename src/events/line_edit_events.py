from PySide6.QtWidgets import QLineEdit
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assets.gui.ui.FolderMasterui_ui import Ui_MainWindow
    from app import MainWindow
    
class LineEditEvents:
    def __init__(self, ui: "Ui_MainWindow", main_window: "MainWindow"):
        self.ui = ui
        self.main_window = main_window
        
    def update_selected_folder(self):
        line_edit = self.ui.line_edit_selected_folder
        path = line_edit.text()
        # Also update the QTreeView to the new structure
        self.main_window.filesystem_viewer.set_folder_path(line_edit, path)