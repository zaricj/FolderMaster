"""
MainWindow — presentation layer only.

Rules:
    - No business logic; no imports from models/ or controllers/.
    - All user interactions become Signals.
    - Public slot methods allow the Controller to drive UI updates.
"""

import os

from PySide6.QtCore import QPoint, QSettings, Qt, Signal, Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFileDialog,
    QHeaderView,
    QMainWindow,
    QMenu,
    QMessageBox,
    QTableWidgetItem,
)

from src.assets.ui.ui_FolderMaster import Ui_MainWindow
from src.views.file_system_view import FileSystemView

# Table columns of the batch list
COL_RULE, COL_EXTENSIONS, COL_FOLDER, COL_TARGET = range(4)
SOURCE_DIR_ROLE = Qt.ItemDataRole.UserRole  # Source folder stored on the rule-name cell


class MainWindow(QMainWindow):

    # ------------------------------------------------------------------
    # View Signals (Semantic User Intentions)
    # ------------------------------------------------------------------
    browse_folder_clicked = Signal(str)
    go_back_clicked = Signal()
    recent_folder_selected = Signal(str)
    list_files_clicked = Signal(str, str)  # Rule name ("" = no rule), source dir
    display_rule_info_clicked = Signal(str, str)  # Rule name, source dir
    save_rule_clicked = Signal(str, str, list)  # Rule name, opt. folder name, extensions list
    add_to_list_clicked = Signal(str, str)  # Source dir, rule name
    context_menu_action_clicked = Signal(str, int)  # Action text, current row
    organize_clicked = Signal(list)  # Batch rows (each carries its own source dir)

    def __init__(self, app_name: str, org_name: str) -> None:
        super().__init__()
        self.settings = QSettings(org_name, app_name)
        self._load_ui_manifest()
        self._configure_widgets()
        self._mount_sub_views()
        self._connect_widget_events()
        self._restore_window_state()

    def _load_ui_manifest(self) -> None:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def _configure_widgets(self) -> None:
        ui = self.ui
        ui.button_back.setEnabled(False)  # Disabled until there is history
        ui.combobox_recent_folders.setPlaceholderText("Select a recent folder...")
        # Long paths must not dictate the window layout; the popup still shows them in full
        for combobox in (ui.combobox_recent_folders, ui.combobox_rules):
            combobox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
            combobox.setMinimumContentsLength(20)
        ui.text_edit_program_output.setReadOnly(True)
        ui.line_edit_selected_folder.setPlaceholderText("Browse or type a folder path and press Enter...")

        # The rule-info button only has a theme icon; fall back to text where none is available
        ui.button_rule_info.setToolTip("Show rule details")
        if ui.button_rule_info.icon().isNull():
            ui.button_rule_info.setText("Info")

        # The header / feature buttons are not implemented yet
        for button in (ui.button_manage_rules, ui.button_app_settings):
            button.setEnabled(False)
            button.setToolTip("Coming soon")

        table = ui.table_widget_batch_rules
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(24)  # Match the compact tree view rows
        table.setShowGrid(False)
        table.setWordWrap(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        table.horizontalHeader().setProperty("showSortIndicator", False)
        # Centered titles drift off-screen in a wide stretched last column
        table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # The header card already separates itself visually; the extra divider line is redundant
        ui.line.hide()

        # Give the form labels one shared width so the input fields line up
        form_labels = (ui.label_rule_name, ui.label_extensions, ui.label_opt_folder)
        for label in form_labels:
            label.ensurePolished()  # Measure with the stylesheet font, not the default one
        label_width = max(label.sizeHint().width() for label in form_labels)
        for label in form_labels:
            label.setMinimumWidth(label_width)

        # Dynamic properties used by the QSS theme
        ui.button_sort.setProperty("variant", "primary")
        ui.button_save_rule.setProperty("variant", "primary")
        ui.button_rule_info.setProperty("variant", "icon")

    def _mount_sub_views(self) -> None:
        """Instantiates helper wrappers passing down the active layout reference."""
        self.file_system_view = FileSystemView(self)

    def _connect_widget_events(self) -> None:
        ui = self.ui
        # Buttons
        ui.button_browse_folder.clicked.connect(self.handle_browse_folder_button_clicked)
        ui.button_back.clicked.connect(self.go_back_clicked)
        ui.button_list_files.clicked.connect(self.handle_list_files_button_clicked)
        ui.button_rule_info.clicked.connect(self.handle_display_rule_info_button_clicked)
        ui.button_save_rule.clicked.connect(self.handle_save_rule_button_clicked)
        ui.button_add_to_list.clicked.connect(self.handle_add_to_list_button_clicked)
        ui.button_sort.clicked.connect(self.handle_button_sort_clicked)
        # Typed path
        ui.line_edit_selected_folder.returnPressed.connect(self.handle_selected_folder_entered)
        # Combobox
        ui.combobox_recent_folders.activated.connect(self.handle_recent_folder_combobox_activated)
        # Context Menu
        ui.table_widget_batch_rules.customContextMenuRequested.connect(self.show_table_widget_context_menu)

    # --------------------------------------------------------
    # Window State Lifecycle
    # --------------------------------------------------------

    def closeEvent(self, event: QCloseEvent) -> None:
        self._save_window_state()
        super().closeEvent(event)

    def _save_window_state(self) -> None:
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

    def _restore_window_state(self) -> None:
        """Called once on construction (showEvent also fires on every un-minimise)."""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)

        # type=list: QSettings on Windows returns a plain str when only one entry was saved
        recent_folders = self.settings.value("recentFolders", [], type=list)
        combobox = self.ui.combobox_recent_folders
        combobox.addItems([str(p) for p in recent_folders if p])
        combobox.setCurrentIndex(-1)  # Show the placeholder; no folder is active on startup

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _current_rule_name(self) -> str:
        """Selected rule name, or "" when the 'Select a rule...' placeholder is active."""
        combobox = self.ui.combobox_rules
        return combobox.currentText() if combobox.currentIndex() > 0 else ""

    def _source_dir(self) -> str:
        return self.ui.line_edit_selected_folder.text().strip()

    # ------------------------------------
    # Context Menu for QTableWidget
    # ------------------------------------

    @Slot(QPoint)
    def show_table_widget_context_menu(self, position: QPoint) -> None:
        """Constructs and displays the context menu locally in view space."""
        table = self.ui.table_widget_batch_rules
        if table.rowCount() == 0:
            return

        # Right-clicking a row should act on that row
        row_under_cursor = table.rowAt(position.y())
        if row_under_cursor >= 0:
            table.selectRow(row_under_cursor)

        menu = QMenu(self)
        remove_selected = menu.addAction("Remove Selected")
        remove_selected.setEnabled(table.currentRow() >= 0)
        menu.addAction("Remove All")

        selected_action = menu.exec(table.viewport().mapToGlobal(position))
        if selected_action:
            self.context_menu_action_clicked.emit(selected_action.text(), table.currentRow())

    @Slot(int)
    def update_table_widget_on_delete_selected(self, selected_row: int) -> None:
        if selected_row >= 0:
            self.ui.table_widget_batch_rules.removeRow(selected_row)

    @Slot()
    def update_table_widget_on_delete_all(self) -> None:
        self.ui.table_widget_batch_rules.setRowCount(0)

    # ------------------------------------
    # Organize button
    # ------------------------------------

    @Slot(str, int)
    def update_on_organize_completed(self, rule_name: str, moved_count: int) -> None:
        self.ui.text_edit_program_output.append(
            f"» Rule '{rule_name}': Processed and moved {moved_count} file(s)."
        )
        self.statusBar().showMessage(f"Rule '{rule_name}': moved {moved_count} file(s)", 5000)

    @Slot()
    def handle_button_sort_clicked(self) -> None:
        """Gathers the entire table data batch and sends it out to the controller."""
        table = self.ui.table_widget_batch_rules

        if table.rowCount() == 0:
            QMessageBox.warning(self, "Empty Batch", "There are no rules in the batch list to organize.")
            return

        batch_data = []
        for row in range(table.rowCount()):
            rule_item = table.item(row, COL_RULE)
            batch_data.append(
                {
                    "rule_name": rule_item.text(),
                    "source_dir": rule_item.data(SOURCE_DIR_ROLE) or self._source_dir(),
                    "extensions": [
                        ext.strip() for ext in table.item(row, COL_EXTENSIONS).text().split(",") if ext.strip()
                    ],
                    "folder": table.item(row, COL_FOLDER).text(),
                }
            )

        answer = QMessageBox.question(
            self,
            "Organize files",
            f"Move matching files for {len(batch_data)} rule(s) into their target folders?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.ui.text_edit_program_output.clear()
            self.organize_clicked.emit(batch_data)

    # ------------------------------------
    # Browse folder
    # ------------------------------------

    @Slot(str)
    def update_on_browse_folder_clicked(self, path: str) -> None:
        self.ui.line_edit_selected_folder.setText(path)
        self.file_system_view.update_displayed_folder(path)

    @Slot()
    def handle_browse_folder_button_clicked(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder", self._source_dir())
        if folder:
            self.browse_folder_clicked.emit(folder)

    @Slot()
    def handle_selected_folder_entered(self) -> None:
        path = self._source_dir()
        if not path:
            return
        if os.path.isdir(path):
            self.browse_folder_clicked.emit(path)
        else:
            self.show_warning_message_box("Directory does not exist", f"The folder does not exist:\n{path}")

    # ------------------------------------
    # List files / rule info
    # ------------------------------------

    @Slot()
    def handle_list_files_button_clicked(self) -> None:
        self.list_files_clicked.emit(self._current_rule_name(), self._source_dir())

    @Slot()
    def handle_display_rule_info_button_clicked(self) -> None:
        self.display_rule_info_clicked.emit(self._current_rule_name(), self._source_dir())

    # ------------------------------------
    # Save rule button
    # ------------------------------------

    @Slot()
    def handle_save_rule_button_clicked(self) -> None:
        rule_name = self.ui.line_edit_rule_name.text().strip()
        opt_folder_name = self.ui.line_edit_opt_folder.text().strip()
        extensions = [ext.strip() for ext in self.ui.line_edit_extensions.text().split(",") if ext.strip()]
        self.save_rule_clicked.emit(rule_name, opt_folder_name, extensions)

    # ------------------------------------
    # Add to list button
    # ------------------------------------

    @Slot()
    def handle_add_to_list_button_clicked(self) -> None:
        self.add_to_list_clicked.emit(self._source_dir(), self._current_rule_name())

    @Slot(str, dict)
    def update_list_widget(self, rule_name: str, rule_data: dict) -> None:
        table = self.ui.table_widget_batch_rules

        source_folder = self._source_dir()
        folder_name = rule_data.get("folder", "")
        extensions = ", ".join(rule_data.get("extensions", []))
        # Mirrors the model: an empty folder name falls back to the rule name
        target_structure = os.path.normpath(os.path.join(source_folder, folder_name or rule_name))

        # Prevent duplicate rows in the batch list
        for row in range(table.rowCount()):
            item_rule = table.item(row, COL_RULE)
            item_target = table.item(row, COL_TARGET)
            if item_rule and item_target and item_rule.text() == rule_name and item_target.text() == target_structure:
                QMessageBox.warning(self, "Duplicate rule", f"The rule '{rule_name}' is already in your batch list.")
                return

        row_idx = table.rowCount()
        table.insertRow(row_idx)

        rule_item = QTableWidgetItem(rule_name)
        rule_item.setData(SOURCE_DIR_ROLE, source_folder)
        target_item = QTableWidgetItem(target_structure)
        target_item.setToolTip(target_structure)

        table.setItem(row_idx, COL_RULE, rule_item)
        table.setItem(row_idx, COL_EXTENSIONS, QTableWidgetItem(extensions))
        table.setItem(row_idx, COL_FOLDER, QTableWidgetItem(folder_name))
        table.setItem(row_idx, COL_TARGET, target_item)

        table.resizeColumnsToContents()

    # ------------------------------------
    # Go back button
    # ------------------------------------

    @Slot(bool)
    def set_back_button_enabled(self, enabled: bool) -> None:
        """Public slot called by the controller to toggle button availability."""
        self.ui.button_back.setEnabled(enabled)

    # ------------------------------------
    # Recent folders combobox
    # ------------------------------------

    @Slot(str, int)
    def update_recent_folders_combobox(self, path: str, max_folders: int) -> None:
        combobox = self.ui.combobox_recent_folders
        items = [combobox.itemText(i) for i in range(combobox.count())]

        # Move the path to the top and enforce the size limit
        items = [path] + [p for p in items if os.path.normcase(p) != os.path.normcase(path)]
        items = items[:max_folders]

        combobox.blockSignals(True)
        combobox.clear()
        combobox.addItems(items)
        combobox.setCurrentIndex(0)
        combobox.blockSignals(False)

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
        previous = combobox.currentText()

        combobox.blockSignals(True)
        combobox.clear()
        combobox.addItem("Select a rule...")
        combobox.addItems(list(rules_data))
        # Keep the user's selection across reloads (e.g. after saving a rule)
        combobox.setCurrentIndex(max(combobox.findText(previous), 0))
        combobox.blockSignals(False)

        if not rules_data:
            self.ui.text_edit_program_output.setPlainText("No rules found to load")

    # ------------------------------------
    # Program Output updates
    # ------------------------------------

    @Slot(list)
    def update_list_files_to_program_output(self, files_list: list[str]) -> None:
        if not files_list:
            self.ui.text_edit_program_output.append("No matching files found.")
            return
        # One append for the whole list is much cheaper than one per file
        self.ui.text_edit_program_output.append("\n".join(f"• {name}" for name in files_list))
        self.statusBar().showMessage(f"{len(files_list)} file(s) found", 5000)

    @Slot(str)
    def update_append_to_program_output(self, message: str) -> None:
        self.ui.text_edit_program_output.append(message)

    @Slot(str)
    def update_set_text_to_program_output(self, message: str) -> None:
        self.ui.text_edit_program_output.setPlainText(message)

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
