from PySide6.QtWidgets import QFileSystemModel, QLineEdit
from PySide6.QtCore import QStandardPaths
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assets.gui.ui.ui_FolderMaster import Ui_MainWindow
    from app import MainWindow

class FileSystemEvents:
    def __init__(self, ui: "Ui_MainWindow", main_window: "MainWindow"):
        self.ui = ui
        self.main_window = main_window
        
    def update_filesystem_view(self, index):
        if index.isValid():
            line_edit = self.ui.line_edit_selected_folder
            path = self.ui.tree_view_folder.model().data(index, QFileSystemModel.FilePathRole)
            self.main_window.filesystem_viewer.set_folder_path(line_edit, path)