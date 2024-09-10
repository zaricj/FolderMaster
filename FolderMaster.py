from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QFileDialog, QMessageBox, QSizePolicy, QTreeView, QFileSystemModel, QGroupBox)
from PySide6.QtGui import QAction, QCloseEvent, QIcon
from PySide6.QtCore import QThread, Signal, QObject, QDir
from pathlib import Path
import os
import sys
import shutil

# //TODO Encapsulate method for organizing file because a wierd bug happens and the method gets initialised on startup and buggs out the GUI

class MainWindow(QMainWindow):
    progress_updated = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Master v1.0")
        self.setWindowIcon(QIcon("_internal\\icon\\icon.ico"))
        self.setGeometry(500, 250, 750, 650)
        self.saveGeometry()
        self.initUI()
        
        # Create the menu bar
        self.create_menu_bar()
        
        # Apply the custom dark theme
        self.apply_custom_dark_theme()
        
        
    def initUI(self):
        # Create the main layout
        main_layout = QVBoxLayout()
        
        # Central widget to hold main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Add the main group to the main layout
        main_layout.addWidget(self.create_main_group())
        main_layout.addWidget(self.create_organize_group())
        main_layout.addWidget(self.create_program_output_and_tree_group())
        
        
    def create_main_group(self):
        group = QGroupBox("Main")
        layout = QVBoxLayout()
        
        # Input folder selection
        inputs_layout = QHBoxLayout()
        
        self.input_folder = QLineEdit()
        self.input_folder.setPlaceholderText("Choose a folder that contains files for organizing...")
        inputs_layout.addWidget(self.input_folder)
        self.input_folder_button = QPushButton("Browse")
        self.input_folder_button.clicked.connect(self.browse_input_folder)
        inputs_layout.addWidget(self.input_folder_button)
        layout.addWidget(QLabel("Select source folder:"))
        layout.addLayout(inputs_layout)
        
        # Output folder selection
        outputs_layout = QHBoxLayout()
        
        self.output_folder = QLineEdit()
        self.output_folder.setPlaceholderText("Choose a folder where to save organized files to...")
        outputs_layout.addWidget(self.output_folder)
        self.output_folder_button = QPushButton("Browse")
        self.output_folder_button.clicked.connect(self.browse_output_folder)
        outputs_layout.addWidget(self.output_folder_button)
        layout.addWidget(QLabel("Select destination folder:"))
        layout.addLayout(outputs_layout)
        
        # Create folder button and input
        create_folder_layout = QHBoxLayout()
        
        self.create_folder_name = QLineEdit()
        self.create_folder_name.setPlaceholderText("Enter name for new folder...")
        self.create_folder_name.setClearButtonEnabled(True)
        create_folder_layout.addWidget(self.create_folder_name)
        self.button_create_folder = QPushButton("Create")
        self.button_create_folder.clicked.connect(self.create_folder_in_destination)
        create_folder_layout.addWidget(self.button_create_folder)
        layout.addWidget(QLabel("Create new folder in destination folder:"))
        layout.addLayout(create_folder_layout)
        
        # List filetypes to list and move
        filetypes_layout = QHBoxLayout()
        combo_list = ["all",".xls",".xlsx",".docx",".pak",".csv",".xml",".zip",".pdf",".txt",".jar",".jpg",".png",".icon",".mp4",".avi",".wav"]
        
        self.filetypes_combobox = QComboBox()
        self.filetypes_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.filetypes_combobox.addItems(combo_list)
        combobox_label = QLabel("File Type:")
        filetypes_layout.addWidget(combobox_label)
        filetypes_layout.addWidget(self.filetypes_combobox)
        self.button_list_files = QPushButton("List Files")
        self.button_list_files.clicked.connect(self.list_files_in_source_folder)
        self.button_list_files.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        filetypes_layout.addWidget(self.button_list_files)
        self.button_move_files = QPushButton("Move Files")
        self.button_move_files.clicked.connect(self.moving_selected_filetype)
        self.button_move_files.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        filetypes_layout.addWidget(self.button_move_files)
        layout.addWidget(QLabel("Select a specific filetype to list or move:"))
        layout.addLayout(filetypes_layout)
        
        group.setLayout(layout)
        return group
        
    
    def create_organize_group(self):
        group = QGroupBox("Organize (Optional)")
        layout = QVBoxLayout()
        
        # Elements
        organize_layout = QHBoxLayout()
        organize_options = ["Images", "Documents", "Archives", "Videos", "Audio"]

        organize_label = QLabel("Select organizing option:")
        organize_layout.addWidget(organize_label)
        self.organize_combobox = QComboBox()
        self.organize_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.organize_combobox.addItems(organize_options)
        organize_layout.addWidget(self.organize_combobox)
        self.button_organize = QPushButton("Organize")
        self.button_organize.clicked.connect(self.organize_files)
        self.button_organize.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        organize_layout.addWidget(self.button_organize)
        
        layout.addWidget(QLabel("Automatic file organization"))
        layout.addLayout(organize_layout)
        
        group.setLayout(layout)
        return group    
        
        
    def create_program_output_and_tree_group(self):
        group = QGroupBox("Output and TreeView")
        layout = QVBoxLayout()
        
        # Program output and Tree View
        program_output_and_treeview_layout = QHBoxLayout()
        
        # Left side: Program Output
        program_output_vertical_layout = QVBoxLayout()
        self.program_output_label = QLabel("Program Output:")
        self.program_output = QTextEdit()
        self.program_output.setReadOnly(True)
        program_output_vertical_layout.addWidget(self.program_output_label)
        program_output_vertical_layout.addWidget(self.program_output)
        
        # Right side: Tree View
        tree_view_vertical_layout = QVBoxLayout()
        self.tree_view_label = QLabel("Tree View:")
        self.tree_view = QTreeView()
        self.tree_view.setDragEnabled(True)  # Enable dragging
        tree_view_vertical_layout.addWidget(self.tree_view_label)
        tree_view_vertical_layout.addWidget(self.tree_view)
        
        # Add both vertical layouts to the horizontal layout
        program_output_and_treeview_layout.addLayout(program_output_vertical_layout)
        program_output_and_treeview_layout.addLayout(tree_view_vertical_layout)
        
        # Add the horizontal layout to the main vertical layout
        layout.addLayout(program_output_and_treeview_layout)
        
        # Set up the file system model
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath("")
        self.file_system_model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        
        # Set the model to the tree view
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.setRootIndex(self.file_system_model.index(""))  # Set root index to the filesystem root
        
        # Optional: Customize the view
        self.tree_view.setColumnWidth(0, 250)  # Adjust column width
        self.tree_view.setHeaderHidden(False)   # Show the header
        self.tree_view.setSortingEnabled(True)  # Enable sorting
        
        group.setLayout(layout)
        return group
    
        
    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(self, "Exit Program", "Are you sure you want to exit the program?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File Menu
        file_menu = menu_bar.addMenu("&File")
        clear_action = QAction("Clear output", self)
        clear_action.setStatusTip("Clear the output")
        clear_action.triggered.connect(self.clear_output)
        file_menu.addAction(clear_action)
        switch_folder =  QAction("Switch source/destination folders", self)
        switch_folder.setStatusTip("Switches Folder Inputs")
        switch_folder.triggered.connect(self.switch_src_dest)
        file_menu.addAction(switch_folder)
        exit_action = QAction("E&xit", self)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Open Menu
        open_menu = menu_bar.addMenu("&Open")
        open_input_action = QAction("Open source folder", self)
        open_input_action.setStatusTip("Opens the log files input folder")
        open_input_action.triggered.connect(self.open_input_folder)
        open_menu.addAction(open_input_action)
        open_output_action = QAction("Open destination folder", self)
        open_output_action.setStatusTip("Opens the zipped archives output folder")
        open_output_action.triggered.connect(self.open_output_folder)
        open_menu.addAction(open_output_action)
        
        # Theme Menu
        theme_menu = menu_bar.addMenu("&Themes")
        #default_theme_action = QAction("Default (Orange)", self)
        #default_theme_action.setStatusTip("Default theme")
        #default_theme_action.triggered.connect(self.apply_custom_dark_theme)
        # theme_menu.addAction(default_theme_action)
        self.ivanas_theme_action = QAction("Ivana's theme", self)
        self.ivanas_theme_action.setStatusTip("Pink theme")
        self.ivanas_theme_action.setCheckable(True)
        self.ivanas_theme_action.triggered.connect(self.theme_changer)
        theme_menu.addAction(self.ivanas_theme_action)
        
    # START Functions START #
    
    # Change theme based of selected theme in menu bar
    def theme_changer(self):
        if self.ivanas_theme_action.isChecked():
            self.ivanas_theme()
        else:
            self.apply_custom_dark_theme()
        
        
    def clear_output(self):
        self.program_output.clear()
        
        
    def switch_src_dest(self):
        try:
            # Get the current values
            input_text = self.input_folder.text()
            output_text = self.output_folder.text()

            # Swap the values
            self.input_folder.setText(output_text)
            self.output_folder.setText(input_text)
        except Exception as e:
            self.program_output.setText(f"Exception occurred: {e}")
            
    # Open Log files input folder 
    def open_input_folder(self):
        directory_path = self.input_folder.text()
        
        if os.path.exists(directory_path):
            try:
                os.startfile(directory_path)
            except Exception as ex:
                message = f"An exception of type {type(ex).__name__} occurred. Arguments: {ex.args!r}"
                QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.warning(self, "Error", f"Path does not exist or is not a valid path:\n{directory_path}")
    
    
    # Open Zipped Archive output folder
    def open_output_folder(self):
        directory_path = self.output_folder.text()
        
        if os.path.exists(directory_path):
            try:
                os.startfile(directory_path)
            except Exception as ex:
                message = f"An exception of type {type(ex).__name__} occurred. Arguments: {ex.args!r}"
                QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.warning(self, "Error", f"Path does not exist or is not a valid path:\n{directory_path}")

    
    def browse_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.input_folder.setText(folder)
            
            
    def browse_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.output_folder.setText(folder)
    
    # Main Group Box Functions
    def list_files_in_source_folder(self):
        combobox_value = self.filetypes_combobox.currentText()
        source = self.input_folder.text()
        
        filetype_actions = {
            ".xls": self.file_type,
            ".xlsx": self.file_type,
            ".mp4": self.file_type,
            ".avi": self.file_type,
            ".wav": self.file_type,
            ".xml": self.file_type,
            ".zip": self.file_type,
            ".pdf": self.file_type,
            ".pak": self.file_type,
            ".jar": self.file_type,
            ".txt": self.file_type,
            ".jpg": self.file_type,
            ".png": self.file_type,
            ".csv": self.file_type,
            ".icon": self.file_type,
            ".docx": self.file_type,
            "all": self.list_all_files
        }
        
        if len(source) > 0:
            if combobox_value in filetype_actions:
                action = filetype_actions[combobox_value]
                filenames = action(combobox_value, source)
                if filenames:
                    self.program_output.setText(f"Files in '{source}':")
                    for filename in filenames:
                        self.program_output.append(filename)
                else:
                    self.program_output.setText("No files found.")
            else:
                self.program_output.setText("Invalid file type selected.")
        else:
            self.program_output.setText("Source folder path is empty.")
    
    
    def file_type(self, ends_with, source):
        sourcefiles = os.listdir(source)
        matched_files = [file for file in sourcefiles if file.endswith(ends_with)]
        return matched_files
    
    
    def list_all_files(self, _, source):
        sourcefiles = os.listdir(source)
        return sourcefiles
    
    
    def moving_selected_filetype(self):
        combobox_value = self.filetypes_combobox.currentText()
        source = self.input_folder.text()
        destination = self.output_folder.text()

        # Clear previous output
        self.program_output.clear()

        try:
            if not source:
                self.program_output.setText("Source Folder is not a valid Path")
                return  # Early exit
            elif not destination:
                self.program_output.setText("Destination Folder is not a valid Path")
                return  # Early exit

            # Gather all files to move
            files_moved = []
            for file in os.listdir(source):
                file_path = os.path.join(source, file)  # Correctly join paths
                if file.endswith(combobox_value):
                    dst_file = os.path.join(destination, file)  # Correctly join paths
                    try:
                        shutil.move(file_path, dst_file)
                        files_moved.append(file)
                    except (FileNotFoundError, PermissionError, FileExistsError, OSError) as e:
                        self.program_output.append(f"Error moving file {file}: {e}")
                elif combobox_value == "all":
                    dst_file = os.path.join(destination, file)  # Correctly join paths
                    try:
                        shutil.move(file_path, dst_file)
                        files_moved.append(file)
                    except (FileNotFoundError, PermissionError, FileExistsError, OSError) as e:
                        self.program_output.append(f"Error moving file {file}: {e}")

            if files_moved:
                self.program_output.setText(f"Moved following Files to '{destination}':\n{',\n'.join(files_moved)}")
            else:
                self.program_output.setText("No files matched the selected type.")

        except Exception as e:
            self.program_output.setText(f"Exception Error: {e}")


    def create_folder_in_destination(self):
        folder_name = self.create_folder_name.text()
        destination = self.output_folder.text()
        try:
            if len(folder_name) > 0:
                path = os.path.join(destination, folder_name)
                os.mkdir(path)
                self.program_output.setText(f"Created folder '{folder_name}' in '{destination}'.\nUpdated destination folder input.")
                self.output_folder.setText(path)
            elif not destination:
                self.program_output.setText("Please set a path for the destination folder.")
            else:
                self.program_output.setText("Please enter a name for the Folder.")
        except FileExistsError:
            self.program_output.setText("Folder already exists.")
    
    # Automatic file organization option
    def organize_files(self):
        organize_option = self.organize_combobox.currentText()
        source = self.input_folder.text()
        print("ASDF")
        try:
            file_types = {
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
                "Documents": [".docx", ".pdf", ".xls", ".xlsx", ".xml", ".txt", ".pptx", ".odt"],
                "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".pak"],
                "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"],
                "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma"],
            }
            
            # Helper function to create folder if not exists
            def create_folder(path):
                if not os.path.exists(path):
                    os.makedirs(path)

            # Iterate through files in the source directory
            if source:
                for file in os.listdir(source):
                    file_path = os.path.join(source, file)

                    if os.path.isfile(file_path):
                        for category, extensions in file_types.items():
                            if any(file.endswith(ext) for ext in extensions) and organize_option == category:
                                folder_path = os.path.join(source, category)
                                create_folder(folder_path)
                                shutil.move(file_path, os.path.join(folder_path, file))
                                break
                        self.program_output.setText(f"Organized files of type '{category}' and moved to path '{folder_path}'")
            else:
                self.program_output.setText("Please choose a source folder for files to organize.")
                       
        except Exception as e:
            self.program_output.setText(f"An exception of type {type(e).__name__} occurred. Arguments: {e.args!r}")
            
        # END Functions END #
        
    # Style
    def apply_custom_dark_theme(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #1c1d21;
            color: #ffffff;
        }
        QWidget {
            background-color: #1c1d21;
            color: #ffffff;
        }
        QLabel {
            color: #ffffff;
            font: bold;
        }
        QLineEdit, QTextEdit, QTreeView {
            background-color: #2a2b2f;
            border: 1px solid #555555;
            padding: 2px;
            color: #ffffff;
        }
        QPushButton {
            background-color: #c17115;
            color: white;
            border: none;
            padding: 5px;
            min-width: 80px;
        }
        QPushButton:hover {
            background-color: #a0650d;
        }
        QPushButton:pressed {
            background-color: #8d5a0f;
        }
        QPushButton:disabled {
            background-color: #808080;
        }
        QTreeView::item:selected {
            background-color: #c17115;
        }
        QMenuBar {
            background-color: #1c1d21;
            color: #ffffff;
        }
        QMenuBar::item:selected {
            background-color: #2a2b2f;
        }
        QMenu {
            background-color: #1c1d21;
            color: #ffffff;
        }
        QMenu::item:selected {
            background-color: #c17115;
        }
        QStatusBar {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font: bold 
        }
        QProgressBar::chunk {
            background-color: #0d47a1;
            width: 10px;
            margin: 0.5px
        }
        """)
        
    def ivanas_theme(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #1c1d21;
            color: #ffffff;
        }
        QWidget {
            background-color: #1c1d21;
            color: #ffffff;
        }
        QLabel {
            color: #ffffff;
            font: bold;
        }
        QLineEdit, QTextEdit, QTreeView {
            background-color: #2a2b2f;
            border: 1px solid #555555;
            padding: 2px;
            color: #ffffff;
        }
        QPushButton {
            background-color: #f579a0;
            color: white;
            border: none;
            padding: 5px;
            min-width: 80px;
        }
        QPushButton:hover {
            background-color: #b95e7b;
        }
        QPushButton:pressed {
            background-color: #9d5168;
        }
        QPushButton:disabled {
            background-color: #808080;
        }
        QTreeView::item:selected {
            background-color: #f579a0;
        }
        QMenuBar {
            background-color: #1c1d21;
            color: #ffffff;
        }
        QMenuBar::item:selected {
            background-color: #2a2b2f;
        }
        QMenu {
            background-color: #1c1d21;
            color: #ffffff;
        }
        QMenu::item:selected {
            background-color: #f579a0;
        }
        QStatusBar {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font: bold 
        }
        QProgressBar::chunk {
            background-color: #0d47a1;
            width: 10px;
            margin: 0.5px
        }
        """)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
