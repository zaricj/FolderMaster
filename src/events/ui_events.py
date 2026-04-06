from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assets.gui.ui.FolderMasterui_ui import Ui_MainWindow
    from app import MainWindow

class UIEvents:
    def __init__(self, ui: "Ui_MainWindow", main_window: "MainWindow"):
        self.ui = ui
        self.main_window = main_window

        # Inject dependencies once
        from core.file_manager import FileManager
        self.file_manager = FileManager()

        # Sub event groups
        from events.button_events import ButtonEvents
        from events.combobox_events import ComboBoxEvents
        from events.line_edit_events import LineEditEvents
        from events.filesystem_events import FileSystemEvents

        self.buttons = ButtonEvents(ui, main_window, self.file_manager)
        self.comboboxes = ComboBoxEvents(ui, main_window)
        self.line_edits = LineEditEvents(ui, main_window)
        self.filesystem = FileSystemEvents(ui, main_window)

    def connect_all(self):
        self.connect_buttons()
        self.connect_comboboxes()
        self.connect_line_edits()
        self.connect_filesystem()

    def connect_buttons(self):
        self.ui.button_browse_folder.clicked.connect(self.buttons.browse_folder)
        self.ui.button_list_files.clicked.connect(self.buttons.list_files)
        self.ui.button_save_rule.clicked.connect(self.buttons.save_rule)

    def connect_comboboxes(self):
        self.ui.combobox_rules.currentIndexChanged.connect(self.comboboxes.rule_changed)
        self.ui.combobox_recent_folders.currentIndexChanged.connect(self.comboboxes.recent_folder_item_changed)
        
    def connect_line_edits(self):
        self.ui.line_edit_selected_folder.textChanged.connect(self.line_edits.update_selected_folder)
    
    def connect_filesystem(self):
        self.ui.tree_view_folder.doubleClicked.connect(self.filesystem.update_filesystem_view)
