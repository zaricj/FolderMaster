from typing import TYPE_CHECKING

from PySide6.QtCore import QDir, QModelIndex, QStandardPaths, Qt
from PySide6.QtWidgets import QFileSystemModel, QHeaderView

if TYPE_CHECKING:
    from src.views.main_window_view import MainWindow

COL_NAME, COL_SIZE, COL_TYPE, COL_DATE = range(4)


class FileSystemView:
    def __init__(self, main_window: "MainWindow", start_path: str | None = None) -> None:
        self.main_window = main_window
        self.ui = main_window.ui
        tree = self.ui.tree_view_folder

        # Built-in Qt display model (strictly UI presentation layer). Parented so Qt owns its lifetime.
        self.file_model = QFileSystemModel(main_window)
        self.file_model.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot | QDir.Filter.AllDirs)
        # Don't resolve symlinks/shortcuts for every entry – noticeably faster on large or network folders
        self.file_model.setResolveSymlinks(False)

        if start_path is None:
            start_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)

        tree.setModel(self.file_model)
        tree.setUniformRowHeights(True)  # Lets the view skip per-row size calculations
        tree.setExpandsOnDoubleClick(False)  # Double-click navigates into the folder instead
        tree.setSortingEnabled(True)
        tree.sortByColumn(COL_NAME, Qt.SortOrder.AscendingOrder)
        tree.setColumnHidden(COL_TYPE, True)
        tree.header().setSectionResizeMode(COL_NAME, QHeaderView.ResizeMode.Interactive)
        tree.setColumnWidth(COL_NAME, 280)

        self.update_displayed_folder(start_path)

        # Forward visual clicks to the MainWindow signals
        tree.doubleClicked.connect(self._on_tree_double_clicked)

    def update_displayed_folder(self, path: str) -> None:
        """Public method called by MainWindow when the Controller dictates an update."""
        self.file_model.setRootPath(path)
        self.ui.tree_view_folder.setRootIndex(self.file_model.index(path))

    def _on_tree_double_clicked(self, index: QModelIndex) -> None:
        """When a user double clicks a folder in the tree, notify the app via signals."""
        if self.file_model.isDir(index):
            self.main_window.browse_folder_clicked.emit(self.file_model.filePath(index))
