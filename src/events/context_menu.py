from typing import TYPE_CHECKING
from PySide6.QtCore import Slot, QPoint
from PySide6.QtWidgets import QMenu

if TYPE_CHECKING:
    from assets.gui.ui.ui_FolderMaster import Ui_MainWindow
    from app import MainWindow

class ContextMenu:
    """Handles all context menu events."""
    
    def __init__(self, ui: "Ui_MainWindow", main_window: "MainWindow"):
        self.ui = ui
        self.main_window = main_window

    @Slot(QPoint)
    def on_show_table_widget_context_menu(self, position: QPoint):
        """Show context menu for XPath list widget."""
        menu = QMenu(self.main_window)
        
        remove_selected_action = menu.addAction("Remove Selected")
        remove_all_action = menu.addAction("Remove All")
        
        action = menu.exec(self.ui.table_widget_batch_rules.mapToGlobal(position))
        
        if action == remove_selected_action:
            self.remove_selected_row()
        elif action == remove_all_action:
            self.remove_all_selected_rows()
            
    def remove_selected_row(self):
        """Remove selected row from the table widget."""
        output = self.main_window.ui.text_edit_program_output
        try:
            table = self.ui.table_widget_batch_rules
            selected_item = table.currentRow()
            if selected_item != -1:
                table.removeRow(selected_item)
                output.append(f"Removed item at row: {selected_item}")
            else:
                output.append("No row selected to delete.")
        except IndexError:
            output.append("Nothing to delete.")
        except Exception as ex:
            message = f"An exception of type {type(ex).__name__} occurred. Arguments: {ex.args!r}"
            output.setText(f"Error removing selected item from table: {message}")
    
    def remove_all_selected_rows(self):
        """Remove all selected rows from the table widget."""
        try:
            table = self.ui.table_widget_batch_rules
            output = self.main_window.ui.text_edit_program_output

            if table.rowCount() > 0:
                table.setRowCount(0)  # Wipes out all data rows safely
                output.setText("Deleted all rows from the table.")
            else:
                output.setText("No rows to delete in table.")

        except Exception as ex:
            message = f"An exception of type {type(ex).__name__} occurred. Arguments: {ex.args!r}"
            self.main_window.ui.text_edit_program_output.setText(f"Error removing all rows from table: {message}")
            