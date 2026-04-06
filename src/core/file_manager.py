# file_manager.py
from PySide6.QtWidgets import QMessageBox
from pathlib import Path
from core.config_handler import ConfigHandler

class FileManager:
    def __init__(self):
        self.config_handler = ConfigHandler()
    
    def list_files(self, source: str, rule_name=""):
        try:
            files = []
            source_path = Path(source)
            if not source_path.exists():
                return []
            if rule_name == "Select a rule...":
                files = [file.name for file in source_path.iterdir() if file.is_file()]
                return files
            else:
                extensions: list = self.config_handler.get_custom_rule(rule_name)
                files = [file.name for file in source_path.iterdir() if file.is_file() and file.suffix in extensions]
            return files
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to list files: {e}")
            return []

    def move_files(self, source, destination, ends_with=""):
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            if not dest_path.exists():
                reply = QMessageBox.warning(None,"Warning", f"Destination folder does not exist: {destination}\nDo you want to create it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    dest_path.mkdir(parents=True)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to create folder: {e}")
            return []
        
        files_moved = []
        for file in source_path.iterdir():
            if file.is_file() and (file.suffix == ends_with or ends_with == "all"):
                dst_file = dest_path / file.name
                try:
                    Path.move(file, dst_file)
                    files_moved.append(file.name)
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Failed to move file {file}: {e}")
        return files_moved
    
    def create_folder(self, path):
        try:
            dest_path = Path(path)
            if not dest_path.exists():
                dest_path.mkdir(parents=True)
        except FileExistsError:
            pass
        return str(dest_path)

    def organize_files(self, source, destination, rule_name, extensions):
        try:
            source_path = Path(source)
            dest_path = Path(destination) / rule_name
            if not source_path.exists() or not dest_path.exists():
                QMessageBox.warning(None, "Warning", "Source or Destination folder does not exist.")
                return []
            
            moved_files = []
            for file in source_path.iterdir():
                if file.is_file() and file.suffix.lower() in extensions:
                    dst_file = dest_path / file.name
                    try:
                        Path.move(file, dst_file)
                        moved_files.append(file.name)
                    except Exception as e:
                        QMessageBox.critical(None, "Error", f"Failed to move file {file}: {e}")
            return moved_files
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to organize files: {e}")
            return []