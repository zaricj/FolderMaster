from PySide6.QtCore import QObject, Slot

from src.views.main_window_view import MainWindow
from src.models.app_model import AppModel


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
        self.model.show_context_menu_requested.connect(self.view.show_table_widget_context_menu)

        # Connect QMessageBox dialog
        self.model.error_occurred.connect(self.view.show_error_message_box)
        self.model.warning_occurred.connect(self.view.show_warning_message_box)
        self.model.info_occurred.connect(self.view.show_info_message_box)

        # Connect Program Output
        self.model.append_to_program_output.connect(self.view.update_append_to_program_output)
        self.model.set_text_to_program_output.connect(self.view.update_set_text_to_program_output)


    @Slot(str, list)
    def on_button_sort_clicked(self, source_dir: str, batch_rules: list[dict]) -> None:
        self.model.handle_organize_requested(source_dir, batch_rules)

    @Slot(str, str, dict)
    def on_folder_creation_confirmed(self, source: str, destination: str, rule_config: dict) -> None:
        self.model.execute_file_organization(source, destination, rule_config)

    @Slot(str)
    def on_context_menu_action_clicked(self, action_text: str) -> None:
        # Snag the active row index from the view right now
        current_row = self.view.ui.table_widget_batch_rules.currentRow()
        # Pass both the text action and the row index into the model logic layer
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
        if not path:
            return
        # Update the core path state & update history stack
        self.model.handle_browse_folder_requested(path)
        # Re-shuffle the combobox items so this one goes to the top (Index 0)
        self.model.handle_recent_folder_update_requested(path, self.model.max_recent_folders)

    @Slot(str)
    def on_browse_folder_button_clicked(self, path: str) -> None:
        self.model.handle_browse_folder_requested(path) # Update the actual core path state & history
        self.model.handle_recent_folder_update_requested(path, self.model.max_recent_folders) # Tell the view to synchronize its structural recent folders list

    @Slot()
    def on_go_back_button_clicked(self) -> None:
        # Pass the intent directly down into the business logic processor
        self.model.handle_go_back_requested()

    @Slot()
    def on_load_rules(self) -> None:
        self.model.handle_load_rules_requested()
