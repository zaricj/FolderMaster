"""
MainWindow — presentation layer only.

Rules:
    - No business logic; no imports from models/ or controllers/.
    - All user interactions become Signals.
    - Public slot methods allow the Controller to drive UI updates.
"""

from PySide6.QtCore import Qt, QSettings, Signal, Slot, QPoint
from PySide6.QtGui import QFont, QCloseEvent, QShowEvent, QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QAbstractItemView,
    QTableWidgetItem,
    QMenu,
)
from src.assets.ui.ui_FolderMaster import Ui_MainWindow
from src.views.file_system_view import FileSystemView


class MainWindow(QMainWindow):
    
    # ------------------------------------------------------------------
    # View Signals (Semantic User Intentions)
    # ------------------------------------------------------------------
    browse_folder_clicked = Signal(str)
    go_back_clicked = Signal()
    recent_folder_selected = Signal(str)
    list_files_clicked = Signal(str, str)
    display_rule_info_clicked = Signal(str, str)
    save_rule_clicked = Signal(str, str, list)  # Source dir, opt. folder name, extensions list
    add_to_list_clicked = Signal(str, str)  # Source dir, rule name
    show_context_menu_requested = Signal(QPoint)
    context_menu_action_clicked = Signal(str)
    organize_clicked = Signal(str, list)

    def __init__(self, app_name: str, org_name: str):
        super().__init__()
        self._load_ui_manifest()
        self._mount_sub_views()
        self._connect_widget_events()
        self.settings = QSettings(org_name, app_name)

    def _load_ui_manifest(self) -> None:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def _mount_sub_views(self) -> None:
        """Instantiates helper wrappers passing down the active layout reference."""
        self.file_system_view = FileSystemView(self)

    def _connect_widget_events(self) -> None:
        # Buttons
        self.ui.button_browse_folder.clicked.connect(self.handle_browse_folder_button_clicked)
        self.ui.button_back.setEnabled(False)  # Disable back button on startup
        self.ui.button_back.clicked.connect(self.handle_go_back_button_clicked)
        self.ui.button_list_files.clicked.connect(self.handle_list_files_button_clicked)
        self.ui.button_rule_info.clicked.connect(self.handle_display_rule_info_button_clicked)
        self.ui.button_save_rule.clicked.connect(self.handle_save_rule_button_clicked)
        self.ui.button_add_to_list.clicked.connect(self.handle_add_to_list_button_clicked)
        self.ui.button_sort.clicked.connect(self.handle_button_sort_clicked)
        # Combobox
        self.ui.combobox_recent_folders.activated.connect(self.handle_recent_folder_combobox_activated)
        # Context Menu
        self.ui.table_widget_batch_rules.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.table_widget_batch_rules.customContextMenuRequested.connect(self.show_table_widget_context_menu)

    # --------------------------------------------------------
    # Window State Lifecycle
    # --------------------------------------------------------

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self._restore_window_state()

    def closeEvent(self, event: QCloseEvent) -> None:
        self._save_window_state()
        super().closeEvent(event)

    def _save_window_state(self) -> None:
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

    def _restore_window_state(self) -> None:
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)

        recent_folders = self.settings.value("recentFolders", [])
        if recent_folders:
            self.ui.combobox_recent_folders.addItems(recent_folders)

    # ------------------------------------------------------------------
    # Internal View Event Handlers (Gathers local UI state, then Emits)
    # ------------------------------------------------------------------

    # ------------------------------------
    # Context Menu for QTableWidget
    # ------------------------------------

    @Slot(QPoint)
    def show_table_widget_context_menu(self, position: QPoint) -> None:
        """Constructs and displays the context menu locally in view space."""
        menu = QMenu(self)

        # Add actions to menu
        menu.addAction("Remove Selected")
        menu.addAction("Remove All")

        # menu.exec() pauses execution and returns the specific QAction clicked
        global_position = self.ui.table_widget_batch_rules.mapToGlobal(position)
        selected_action = menu.exec(global_position)

        # If the user clicked outside the menu, selected_action will be None
        if selected_action:
            # Emit the text string directly to the Controller ("Remove Selected" or "Remove All")
            self.context_menu_action_clicked.emit(selected_action.text())

    @Slot(int)
    def update_table_widget_on_delete_selected(self, selected_row: int) -> None:
        table = self.ui.table_widget_batch_rules
        if selected_row != -1:
            table.removeRow(selected_row)

    @Slot()
    def update_table_widget_on_delete_all(self) -> None:
        table = self.ui.table_widget_batch_rules
        if table.rowCount() > 0:
            table.setRowCount(0)  # Wipes out all data rows safely

    # ------------------------------------
    # Organize button
    # ------------------------------------

    @Slot(str, int)
    def update_on_organize_completed(self, rule_name: str, moved_count: int) -> None:
        """Appends clear logs tracking exactly what row criteria swept up matching items."""
        self.ui.text_edit_program_output.append(
            f"» Rule '{rule_name}': Processed and moved {moved_count} file(s)."
        )

    @Slot()
    def handle_button_sort_clicked(self) -> None:
        """Gathers the entire table data batch and sends it out to the controller."""
        source_dir = self.ui.line_edit_selected_folder.text()
        table = self.ui.table_widget_batch_rules

        if table.rowCount() == 0:
            QMessageBox.warning(
                self, "Empty Batch", "There are no rules in the batch list to organize."
            )
            return

        batch_data = []
        for row in range(table.rowCount()):
            rule_name = table.item(row, 0).text()
            extensions = [
                ext.strip()
                for ext in table.item(row, 1).text().split(",")
                if ext.strip()
            ]
            folder_name = table.item(row, 2).text()

            batch_data.append(
                {
                    "rule_name": rule_name,
                    "extensions": extensions,
                    "folder": folder_name,
                }
            )

        self.organize_clicked.emit(source_dir, batch_data)

    # ------------------------------------
    # Browse folder button
    # ------------------------------------

    @Slot(str)  # Browse button
    def update_on_browse_folder_clicked(self, path: str) -> None:
        self.ui.line_edit_selected_folder.setText(path)
        self.file_system_view.update_displayed_folder(path)

    @Slot()
    def handle_browse_folder_button_clicked(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.browse_folder_clicked.emit(folder)

    # ------------------------------------
    # List files button
    # ------------------------------------

    @Slot()
    def handle_list_files_button_clicked(self) -> None:
        rule_name = self.ui.combobox_rules.currentText()
        source_dir = self.ui.line_edit_selected_folder.text()
        self.list_files_clicked.emit(rule_name, source_dir)

    # ------------------------------------
    # Display rule info button
    # ------------------------------------

    @Slot()
    def handle_display_rule_info_button_clicked(self) -> None:
        rule_name = self.ui.combobox_rules.currentText()
        source_dir = self.ui.line_edit_selected_folder.text()
        self.display_rule_info_clicked.emit(rule_name, source_dir)

    # ------------------------------------
    # Save rule button
    # ------------------------------------

    @Slot()
    def handle_save_rule_button_clicked(self) -> None:
        rule_name: str = self.ui.line_edit_rule_name.text().strip()
        opt_folder_name: str = self.ui.line_edit_opt_folder.text().strip()
        # Split extensions by comma and strip extra whitespaces from each entry
        extensions: list[str] = [
            ext.strip()
            for ext in self.ui.line_edit_extensions.text().split(",")
            if ext.strip()
        ]
        self.save_rule_clicked.emit(rule_name, opt_folder_name, extensions)

    # ------------------------------------
    # Add to list button
    # ------------------------------------

    @Slot(int)
    def remove_table_row_at(self, row_index: int) -> None:
        self.ui.table_widget_batch_rules.removeRow(row_index)

    @Slot()
    def clear_all_table_rows(self) -> None:
        self.ui.table_widget_batch_rules.setRowCount(0)

    @Slot()
    def handle_add_to_list_button_clicked(self) -> None:
        source_dir = self.ui.line_edit_selected_folder.text()
        rule_name = self.ui.combobox_rules.currentText()
        self.add_to_list_clicked.emit(source_dir, rule_name)

    @Slot(str, dict)
    def update_list_widget(self, rule_name: str, rule_data: dict) -> None:
        table = self.ui.table_widget_batch_rules
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Extract the data for this specific rule
        source_folder = self.ui.line_edit_selected_folder.text()
        folder_name = rule_data.get("folder", "")
        extensions = ", ".join(rule_data.get("extensions", []))
        target_structure = (source_folder if folder_name == "" else f"{source_folder}/{folder_name}")
        
        # Prevent duplicate rows in the batch list
        for row in range(table.rowCount()):
            item_rule = table.item(row, 0)
            item_target = table.item(row, 3)

            if not item_rule or not item_target:
                continue

            if item_rule.text() == rule_name and item_target.text() == target_structure:
                QMessageBox.warning(
                    self,
                    "Duplicate rule",
                    f"The rule '{rule_name}' is already in your batch list.",
                )
                return

        # Insert exactly ONE new row at the bottom of your table
        row_idx = table.rowCount()
        table.insertRow(row_idx)

        # Populate the cells for this rule
        table.setItem(row_idx, 0, QTableWidgetItem(rule_name))              # Column 0: Rule Name
        table.setItem(row_idx, 1, QTableWidgetItem(extensions))             # Column 1: Extensions
        table.setItem(row_idx, 2, QTableWidgetItem(folder_name))            # Column 2: Opt. Folder Name
        table.setItem(row_idx, 3, QTableWidgetItem(str(target_structure)))  # Column 3: Target Structure

        # Automatically fit column widths cleanly
        table.resizeColumnsToContents()

    # ------------------------------------
    # Go back button
    # ------------------------------------

    @Slot()  # Go back button
    def handle_go_back_button_clicked(self) -> None:
        # Simply announce the intentional interaction to the Controller
        self.go_back_clicked.emit()

    @Slot(bool)  # Go back button update state
    def set_back_button_enabled(self, enabled: bool) -> None:
        """Public slot called by the controller to toggle button availability."""
        self.ui.button_back.setEnabled(enabled)

    # ------------------------------------
    # Recent folders combobox
    # ------------------------------------

    @Slot(str, int)  # Recent folders combobox
    def update_recent_folders_combobox(self, path: str, max_folders: int) -> None:
        combobox = self.ui.combobox_recent_folders

        # Extract clean list of current items
        items = [combobox.itemText(i) for i in range(combobox.count())]

        # If it already exists, remove it so we can re-insert it at the top
        if path in items:
            index = items.index(path)
            combobox.removeItem(index)
            items.remove(path)

        # Enforce max folders constraint by popping old items
        while len(items) >= max_folders:
            combobox.removeItem(combobox.count() - 1)
            items.pop()

        # Insert newest path cleanly at the top (Index 0)
        combobox.insertItem(0, path)
        combobox.setCurrentIndex(0)
        items.insert(0, path)

        # Persist state and notify
        self.settings.setValue("recentFolders", items)

    @Slot(int)
    def handle_recent_folder_combobox_activated(self, index: int) -> None:
        """Fires only when the user manually clicks an item in the dropdown list."""
        path = self.ui.combobox_recent_folders.itemText(index)
        if path:
            self.recent_folder_selected.emit(path)

    # ------------------------------------
    # Rules combobox load
    # ------------------------------------

    @Slot(dict)
    def update_rules_combobox(self, rules_data: dict) -> None:
        combobox = self.ui.combobox_rules
        combobox.clear()
        combobox.addItem("Select a rule...")

        if not rules_data:
            self.ui.text_edit_program_output.setText("No rules found to load")
        else:
            rules: list[str] = list(rules_data.keys())
            combobox.addItems(rules)

    # ------------------------------------
    # Program Output updates
    # ------------------------------------

    @Slot(list)  # List files button update program output with files
    def update_list_files_to_program_output(self, files_list: list[str]) -> None:

        if not files_list:
            self.ui.text_edit_program_output.setText(
                "No matching files found for this rule."
            )
            return
        formatted_text = "\n".join(f"• {filename}" for filename in files_list)

        # Display it in your UI element
        self.ui.text_edit_program_output.append(formatted_text)

    @Slot(str)  # Program Output append
    def update_append_to_program_output(self, message: str) -> None:
        self.ui.text_edit_program_output.append(message)

    @Slot(str)  # Program Output setText
    def update_set_text_to_program_output(self, message: str) -> None:
        self.ui.text_edit_program_output.setText(message)

    # ------------------------------------
    # QMessageBox slots
    # ------------------------------------

    @Slot(str, str)
    def show_error_message_box(self, title: str, message: str) -> None:
        QMessageBox.critical(self, title, message)

    @Slot(str, str)
    def show_warning_message_box(self, title: str, message: str) -> None:
        QMessageBox.warning(self, title, message)

    @Slot(str, str)
    def show_info_message_box(self, title: str, message: str) -> None:
        QMessageBox.information(self, title, message)
