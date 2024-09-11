import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QTextEdit, QVBoxLayout, QWidget, QFileDialog, QMessageBox,
    QHBoxLayout, QLineEdit, QPushButton, QLabel, QColorDialog, QTreeView, QMenuBar, QStatusBar,
    QProgressBar, QSplitter
)
from PySide6.QtCore import QFile, QTextStream, Qt
from PySide6.QtGui import QAction, QColor, QStandardItemModel, QStandardItem

class ColorInput(QWidget):
    def __init__(self, label, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.label = QLabel(label)
        self.color_input = QLineEdit()
        self.color_button = QPushButton("Pick Color")
        self.color_button.clicked.connect(self.pick_color)
        layout.addWidget(self.label)
        layout.addWidget(self.color_input)
        layout.addWidget(self.color_button)
        self.setLayout(layout)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_input.setText(color.name())

class PreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # QLabel
        self.label = QLabel("Preview Label")
        layout.addWidget(self.label)

        # QLineEdit
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Preview Line Edit")
        layout.addWidget(self.line_edit)

        # QTextEdit
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Preview Text Edit")
        layout.addWidget(self.text_edit)

        # QTreeView
        self.tree_view = QTreeView()
        model = QStandardItemModel()
        root_item = model.invisibleRootItem()
        item1 = QStandardItem("Item 1")
        item2 = QStandardItem("Item 2")
        item1.appendRow(QStandardItem("Subitem 1"))
        root_item.appendRow(item1)
        root_item.appendRow(item2)
        self.tree_view.setModel(model)
        layout.addWidget(self.tree_view)

        # QPushButton (normal, hover, pressed, disabled)
        button_layout = QHBoxLayout()
        self.normal_button = QPushButton("Normal")
        self.hover_button = QPushButton("Hover")
        self.pressed_button = QPushButton("Pressed")
        self.disabled_button = QPushButton("Disabled")
        self.disabled_button.setEnabled(False)
        button_layout.addWidget(self.normal_button)
        button_layout.addWidget(self.hover_button)
        button_layout.addWidget(self.pressed_button)
        button_layout.addWidget(self.disabled_button)
        layout.addLayout(button_layout)

        # QMenuBar
        self.menu_bar = QMenuBar()
        file_menu = self.menu_bar.addMenu("File")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        layout.addWidget(self.menu_bar)

        # QStatusBar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Status Bar")
        layout.addWidget(self.status_bar)

        # QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(50)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Stylesheet Editor")

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left side: editor and color inputs
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Enter your custom stylesheet here...")
        left_layout.addWidget(self.editor)

        # Color inputs
        self.background_color = ColorInput("Background Color:")
        self.text_color = ColorInput("Text Color:")
        self.button_color = ColorInput("Button Color:")
        left_layout.addWidget(self.background_color)
        left_layout.addWidget(self.text_color)
        left_layout.addWidget(self.button_color)

        # Apply colors button
        apply_colors_button = QPushButton("Apply Colors")
        apply_colors_button.clicked.connect(self.apply_colors)
        left_layout.addWidget(apply_colors_button)

        left_widget.setLayout(left_layout)

        # Right side: preview
        self.preview_widget = PreviewWidget()

        # Use QSplitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(self.preview_widget)
        splitter.setSizes([400, 400])  # Set initial sizes

        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Set up the menu
        self.create_menu()

        # Load the default stylesheet
        self.load_stylesheet("default.qss")

    def create_menu(self):
        # Create the menu bar
        menu_bar = self.menuBar()
        # Add 'Stylesheet' menu
        stylesheet_menu = menu_bar.addMenu("Stylesheet")
        # Action to apply stylesheet
        apply_action = QAction("Apply Stylesheet", self)
        apply_action.triggered.connect(self.apply_stylesheet)
        stylesheet_menu.addAction(apply_action)
        # Action to load stylesheet from file
        load_action = QAction("Load Stylesheet", self)
        load_action.triggered.connect(self.load_stylesheet_from_file)
        stylesheet_menu.addAction(load_action)
        # Action to save stylesheet to file
        save_action = QAction("Save Stylesheet", self)
        save_action.triggered.connect(self.save_stylesheet_to_file)
        stylesheet_menu.addAction(save_action)
        # Option to reset stylesheet to default
        reset_action = QAction("Reset to Default", self)
        reset_action.triggered.connect(self.reset_to_default)
        stylesheet_menu.addAction(reset_action)

    def apply_stylesheet(self):
        # Get the stylesheet from the editor and apply it
        stylesheet = self.editor.toPlainText()
        self.setStyleSheet(stylesheet)
        self.preview_widget.setStyleSheet(stylesheet)

    def load_stylesheet(self, file_name):
        # Load a stylesheet from a .qss file
        try:
            with QFile(file_name) as file:
                if file.open(QFile.ReadOnly | QFile.Text):
                    stream = QTextStream(file)
                    stylesheet = stream.readAll()
                    self.setStyleSheet(stylesheet)
                    self.editor.setPlainText(stylesheet)  # Load into editor
                    self.preview_widget.setStyleSheet(stylesheet)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load stylesheet: {e}")

    def load_stylesheet_from_file(self):
        # Let the user select a stylesheet file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Stylesheet", "", "Stylesheet Files (*.qss)")
        if file_name:
            self.load_stylesheet(file_name)

    def save_stylesheet_to_file(self):
        # Let the user save the current stylesheet to a file
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Stylesheet", "", "Stylesheet Files (*.qss)")
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.editor.toPlainText())
                QMessageBox.information(self, "Success", "Stylesheet saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save stylesheet: {e}")

    def reset_to_default(self):
        # Reset the stylesheet to the default
        self.load_stylesheet("default.qss")

    def apply_colors(self):
        background_color = self.background_color.color_input.text()
        text_color = self.text_color.color_input.text()
        button_color = self.button_color.color_input.text()

        stylesheet = f"""
        QMainWindow, QWidget {{
            background-color: {background_color};
            color: {text_color};
        }}
        QPushButton {{
            background-color: {button_color};
            color: {background_color};
        }}
        """

        self.editor.setPlainText(self.editor.toPlainText() + "\n" + stylesheet)
        self.apply_stylesheet()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(1000, 800)
    main_window.show()
    sys.exit(app.exec())