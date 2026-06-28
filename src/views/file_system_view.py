from PySide6.QtWidgets import QFileSystemModel
from PySide6.QtCore import QStandardPaths, QModelIndex
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.views.main_window_view import MainWindow


class FileSystemView:
    def __init__(self, main_window: "MainWindow", start_path: str | None = None):
        self.main_window = main_window
        self.ui = main_window.ui

        # Setup the built-in Qt display model (strictly UI presentation layer)
        self.file_model = QFileSystemModel()

        if start_path is None:
            start_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)

        self.file_model.setRootPath(start_path)
        self.ui.tree_view_folder.setModel(self.file_model)

        # Configure View aesthetics
        self.ui.tree_view_folder.setSortingEnabled(True)
        self.ui.tree_view_folder.setColumnHidden(2, True)  # Hide Type column
        self.ui.tree_view_folder.setColumnWidth(0, 200)

        # Set initial visual folder
        self.update_displayed_folder(start_path)

        # 2. Forward visual clicks to the MainWindow signals
        self.ui.tree_view_folder.doubleClicked.connect(self._on_tree_double_clicked)

    def update_displayed_folder(self, path: str) -> None:
        """Public method called by MainWindow when the Controller dictates an update."""
        self.file_model.setRootPath(path)
        index = self.file_model.index(path)
        self.ui.tree_view_folder.setRootIndex(index)

    def _on_tree_double_clicked(self, index: QModelIndex) -> None:
        """When a user double clicks a folder in the tree, notify the app via signals."""
        path = self.file_model.filePath(index)
        if self.file_model.isDir(index):
            self.main_window.browse_folder_clicked.emit(path)
