from PySide6.QtCore import QObject, Slot

from src.models.app_model import AppModel
from src.views.main_window_view import MainWindow


class MainController(QObject):
    def __init__(self, view: MainWindow, model: AppModel, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.view = view
        self.model = model
        self._connect_all_events()
        self.on_load_rules()

    def _connect_all_events(self) -> None:
        # View Actions -> Controller Slots
        self.view.browse_folder_clicked.connect(self.on_browse_folder_button_clicked)
        self.view.go_back_clicked.connect(self.on_go_back_button_clicked)
        self.view.recent_folder_selected.connect(self.on_recent_folder_combobox_activated)
        self.view.list_files_clicked.connect(self.on_list_files_button_clicked)
        self.view.display_rule_info_clicked.connect(self.on_display_rule_button_clicked)
        self.view.save_rule_clicked.connect(self.on_save_rules_clicked)
        self.view.add_to_list_clicked.connect(self.on_add_to_list_clicked)
        self.view.context_menu_action_clicked.connect(self.on_context_menu_action_clicked)
        self.view.organize_clicked.connect(self.on_button_sort_clicked)

        # Model State Mutations -> View Update Slots
        self.model.browse_folder_requested.connect(self.view.update_on_browse_folder_clicked)
        self.model.recent_folder_update_requested.connect(self.view.update_recent_folders_combobox)
        self.model.back_button_state_changed.connect(self.view.set_back_button_enabled)
        self.model.list_files_requested.connect(self.view.update_list_files_to_program_output)
        self.model.load_rules_requested.connect(self.view.update_rules_combobox)
        self.model.add_to_list_requested.connect(self.view.update_list_widget)
        self.model.organize_completed.connect(self.view.update_on_organize_completed)

        # QTableWidget Batch Rules
        self.model.remove_row_requested.connect(self.view.update_table_widget_on_delete_selected)
        self.model.clear_all_rows_requested.connect(self.view.update_table_widget_on_delete_all)

        # QMessageBox dialogs
        self.model.error_occurred.connect(self.view.show_error_message_box)
        self.model.warning_occurred.connect(self.view.show_warning_message_box)
        self.model.info_occurred.connect(self.view.show_info_message_box)

        # Program Output
        self.model.append_to_program_output.connect(self.view.update_append_to_program_output)
        self.model.set_text_to_program_output.connect(self.view.update_set_text_to_program_output)

    @Slot(list)
    def on_button_sort_clicked(self, batch_rules: list[dict]) -> None:
        self.model.handle_organize_requested(batch_rules)

    @Slot(str, int)
    def on_context_menu_action_clicked(self, action_text: str, current_row: int) -> None:
        self.model.handle_context_menu_action_requested(action_text, current_row)

    @Slot(str, str)
    def on_add_to_list_clicked(self, source_dir: str, rule_name: str) -> None:
        self.model.handle_add_to_list_requested(source_dir, rule_name)

    @Slot(str, str, list)
    def on_save_rules_clicked(self, rule_name: str, opt_folder_name: str, extensions: list[str]) -> None:
        self.model.handle_save_rule_requested(rule_name, opt_folder_name, extensions)

    @Slot(str, str)
    def on_display_rule_button_clicked(self, rule_name: str, source_dir: str) -> None:
        self.model.handle_display_rule_info_requested(rule_name, source_dir)

    @Slot(str, str)
    def on_list_files_button_clicked(self, rule_name: str, source_dir: str) -> None:
        self.model.handle_list_files_requested(rule_name, source_dir)

    @Slot(str)
    def on_recent_folder_combobox_activated(self, path: str) -> None:
        """Handles when a user manually picks a path from the recent list."""
        self._open_folder(path)

    @Slot(str)
    def on_browse_folder_button_clicked(self, path: str) -> None:
        self._open_folder(path)

    def _open_folder(self, path: str) -> None:
        if not path:
            return
        # Update the core path state & history, then move the entry to the top of the recent list
        self.model.handle_browse_folder_requested(path)
        self.model.handle_recent_folder_update_requested(path, self.model.max_recent_folders)

    @Slot()
    def on_go_back_button_clicked(self) -> None:
        self.model.handle_go_back_requested()

    @Slot()
    def on_load_rules(self) -> None:
        self.model.handle_load_rules_requested()
