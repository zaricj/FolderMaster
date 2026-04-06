from assets.gui.ui.FolderMasterui_ui import Ui_MainWindow
from core.config_handler import ConfigHandler
from core.filesystem_model import FileSystemViewer
from events.ui_events import UIEvents

import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QFileDialog, QMessageBox, QSizePolicy, QTreeView, QFileSystemModel, QGroupBox, QInputDialog)
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QGuiApplication
from PySide6.QtCore import QThread, Signal, QObject, QDir, QFile, QTextStream, QSettings



def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

# ----------------------------
# Helpers for window state
# ----------------------------

def save_window_state(window: QMainWindow, settings: QSettings):
    settings.setValue("geometry", window.saveGeometry())
    settings.setValue("windowState", window.saveState())


def restore_window_state(window: QMainWindow, settings: QSettings):
    geometry = settings.value("geometry")
    if geometry:
        window.restoreGeometry(geometry)
    state = settings.value("windowState")
    if state:
        window.restoreState(state)

    # Clamp window into current screen space
    screen = QGuiApplication.primaryScreen()
    available = screen.availableGeometry()
    win_geom = window.frameGeometry()

    if not available.contains(win_geom, proper=False):
        window.resize(
            min(win_geom.width(), available.width()),
            min(win_geom.height(), available.height())
        )
        window.move(
            max(available.left(), min(win_geom.left(),
                available.right() - window.width())),
            max(available.top(), min(win_geom.top(),
                available.bottom() - window.height()))
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.filesystem_viewer = FileSystemViewer(self)
        self.config_handler = ConfigHandler()

        # UI event handler for all widgets
        self.events = UIEvents(self.ui, self)
        self.events.connect_all()
        
        self.settings = QSettings("Jovan", "FolderMaster")

        # Rules and config setup
        self.setup_configuration(self.config_handler.config)

        self._load_app_settings(self.settings)
        
    # ===== Load and set up the configuration/rule file =====
    def setup_configuration(self, configuration: dict):
        combobox = self.ui.combobox_rules
        rules: list[str] = list(configuration.keys())
        
        # Add rules to the "rules combobox"
        combobox.addItems(rules)
        
    def save_recent_folders(self, folder_path: str):
        """
        Save a folder to recent folders with a max of 10 items.
        When adding beyond 10 items, rotate through indices 1-9.
        """
        MAX_RECENT_FOLDERS = 10
        combobox = self.ui.combobox_recent_folders
        combobox_items = [combobox.itemText(i) for i in range(combobox.count())]
        
        # If folder already exists, remove it (we'll re-add it as the latest)
        if folder_path in combobox_items:
            index = combobox_items.index(folder_path)
            combobox.removeItem(index)
            combobox_items.remove(folder_path)
        
        # If we're at max capacity, replace the item at the rotating position
        if len(combobox_items) >= MAX_RECENT_FOLDERS:
            # Calculate which index to replace (1-9, rotating)
            replace_index = ((len(combobox_items) - MAX_RECENT_FOLDERS) % (MAX_RECENT_FOLDERS - 1)) + 1
            combobox.setItemText(replace_index, folder_path)
            combobox_items[replace_index] = folder_path
        else:
            # Haven't reached max yet, just add it
            combobox.addItem(folder_path)
            combobox_items.append(folder_path)
        
        self.settings.setValue("recentFolders", combobox_items)
        self.ui.text_edit_program_output.append(f"Added {folder_path} to recent folders!")
    
    def update_recent_folders(self, folders):
        """
        Update the recent folders combobox from a list of folder paths.
        Limits to 10 most recent folders.
        """
        MAX_RECENT_FOLDERS = 10
        combobox = self.ui.combobox_recent_folders
        combobox.clear()
        
        # Add folders up to the max limit
        for folder in folders[:MAX_RECENT_FOLDERS]:
            combobox.addItem(folder)
        

    # ===== Save app settings and close event ===== #
    
    def _load_app_settings(self, settings: QSettings):
        restore_window_state(self, settings)
        recent_folders = settings.value("recentFolders", type=list) or []
        self.update_recent_folders(recent_folders)

    def _save_app_settings(self):
        """Saves app settings to QSettings"""
        recent_folders = [self.ui.combobox_recent_folders.itemText(i) for i in range(self.ui.combobox_recent_folders.count())]
        
        self.settings.setValue("recentFolders", recent_folders)
        save_window_state(self, self.settings)

    def closeEvent(self, event):
        self._save_app_settings()
        # if self._active_worker and self._active_worker.isRunning():
        #     reply = QMessageBox.question(
        #         self,
        #         "Exit Confirmation",
        #         "A task is still running. Are you sure you want to exit?",
        #         QMessageBox.Yes | QMessageBox.No,
        #         QMessageBox.No,
        #     )
        #     if reply == QMessageBox.No:
        #         event.ignore()
        #         return
            # else:
            #     self._active_worker.stop()  # Assuming the worker has a stop method

        super().closeEvent(event)
        
        
if __name__ == "__main__":
    raise SystemExit(main())