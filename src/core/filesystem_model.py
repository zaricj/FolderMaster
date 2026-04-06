from PySide6.QtWidgets import QFileSystemModel, QLineEdit
from PySide6.QtCore import QStandardPaths

from typing import TYPE_CHECKING

from pathlib import Path

if TYPE_CHECKING:
    from app import MainWindow


class FileSystemViewer:

    def __init__(self, main_window: "MainWindow", start_path=None):
        self.main_window = main_window
        self.ui = main_window.ui
        self.start_path = start_path

        # History stack for navigation
        self._history = []
        self._history_index = -1

        # 1. Setup the Model
        self.model = QFileSystemModel()

        if self.start_path is None:
            self.start_path = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.HomeLocation
            )
        else:
            self.start_path = str(self.start_path)

        self.ui.combobox_recent_folders.addItem(self.start_path)

        self.model.setRootPath(self.start_path)
        self.ui.tree_view_folder.setModel(self.model)

        root_index = self.model.index(self.start_path)
        self.ui.tree_view_folder.setRootIndex(root_index)

        self.ui.tree_view_folder.setSortingEnabled(True)
        self.ui.tree_view_folder.setHeaderHidden(False)
        self.ui.tree_view_folder.setColumnHidden(1, False)
        self.ui.tree_view_folder.setColumnHidden(2, True)
        self.ui.tree_view_folder.setColumnHidden(3, False)
        self.ui.tree_view_folder.setColumnWidth(0, 200)

        # Connect back button if it exists in the UI
        # FIX: hasattr check now matches the actual widget name (button_back)
        if hasattr(self.ui, "button_back"):
            self.ui.button_back.clicked.connect(self.go_back)
            self.ui.button_back.setEnabled(False)  # start disabled

        # Push initial folder to history
        self._push_history(self.start_path)

    def is_folder(self, path: str) -> bool:
        return Path(path).is_dir()

    def _update_back_button(self):
        """Enable or disable the back button based on history position."""
        if hasattr(self.ui, "button_back"):
            self.ui.button_back.setEnabled(self._history_index > 0)

    def _apply_path(self, path: str):
        """
        Internal: update the tree view and line edit to reflect a path,
        without pushing to history. Used by both set_root_path and go_back.
        """
        self.model.setRootPath(path)
        root_index = self.model.index(path)
        self.ui.tree_view_folder.setRootIndex(root_index)

        # Sync the line edit so the displayed path always matches the view
        self.ui.line_edit_selected_folder.setText(path)

    def set_root_path(self, path: str):
        """
        Navigate to a new folder, updating the view and pushing to history.
        """
        if not self.is_folder(path):
            return

        self._apply_path(path)
        self._push_history(path)

    def set_folder_path(self, line_edit: QLineEdit, path: str = None):
        """
        Sets the selected folder in the QLineEdit and navigates to it.
        Called when the user double-clicks a folder in the tree view.
        """
        if path and self.is_folder(path):
            line_edit.setText(path)
            self.set_root_path(path)

    # --- History methods ---

    def _push_history(self, path: str):
        """
        Push a new folder to the history stack and manage the index.
        Truncates any forward history if the user navigated back before this.
        """
        # Avoid duplicate consecutive entries
        if self._history_index >= 0 and self._history[self._history_index] == path:
            return

        # Cut off any forward history
        self._history = self._history[: self._history_index + 1]

        self._history.append(path)
        self._history_index += 1

        self._update_back_button()

    def go_back(self):
        """
        Navigate to the previous folder in history.
        Updates the tree view and line edit without pushing a new history entry.
        """
        if self._history_index <= 0:
            return

        self._history_index -= 1
        path = self._history[self._history_index]

        # FIX: use _apply_path so the model root and line edit both update,
        # but do NOT call set_root_path (that would push to history again)
        self._apply_path(path)
        self._update_back_button()