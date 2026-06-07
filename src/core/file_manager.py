from assets.gui.ui.dialogs import info, warning, error
from PySide6.QtWidgets import QMessageBox
from pathlib import Path
from shutil import move
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assets.gui.ui.ui_FolderMaster import Ui_MainWindow
    from app import MainWindow

class FileManager:
    def __init__(self, ui: "Ui_MainWindow", main_window: "MainWindow"):
        self.ui = ui
        self.main_window = main_window
    
    def list_files(self, source: str, rule_name="") -> list[str]:
        try:
            source_path = Path(source)
            if not source_path.exists() or not source_path.is_dir():
                return []
                
            if not rule_name or rule_name == "Select a rule...":
                return []
            
            rule_data = self.main_window.config_handler.get_custom_rule(rule_name)
            if isinstance(rule_data, dict):
                extensions = rule_data.get("extensions", [])
            else:
                extensions = rule_data
                
            extensions = [ext.lower() for ext in extensions]
            
            files = [
                file.name for file in source_path.iterdir() 
                if file.is_file() and file.suffix.lower() in extensions
            ]
            return files
            
        except Exception as e:
            error(None, "Error", f"Failed to list files: {e}")
            return []

    def move_files(self, source: str, destination: str, ends_with="") -> list[str]:
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                warning(None, "Warning", f"Source folder does not exist: {source}")
                return []
                
            if not dest_path.exists():
                reply = warning(
                    None, "Warning", 
                    f"Destination folder does not exist: {destination}\nDo you want to create it?", 
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    dest_path.mkdir(parents=True, exist_ok=True)
                else:
                    return []
                    
        except Exception as e:
            error(None, "Error", f"Failed to verify/create folder: {e}")
            return []
        
        files_moved = []
        ends_with_lower = ends_with.lower()
        
        for file in source_path.iterdir():
            if file.is_file() and (file.suffix.lower() == ends_with_lower or ends_with_lower == "all"):
                dst_file = dest_path / file.name
                try:
                    move(str(file), str(dst_file))
                    files_moved.append(file.name)
                except Exception as e:
                    error(None, "Error", f"Failed to move file {file.name}: {e}")
                    
        return files_moved
    
    def create_folder(self, path: str) -> str:
        try:
            dest_path = Path(path)
            dest_path.mkdir(parents=True, exist_ok=True)
            return str(dest_path)
        except Exception as e:
            error(None, "Error", f"Failed to create folder: {e}")
            return ""

    def organize_files(
        self,
        source: str,
        destination: str,
        rule_name: str,
        rule_config: dict
    ) -> list[str]:
        """
        Organizes files based on rules.json configuration.
        
        rule_config expects: {"extensions": [...], "folder": "optional_name"}
        """
        try:
            source_path = Path(source)
            if not source_path.exists():
                warning(None, "Warning", "Source folder does not exist.")
                return []

            # Safely extract extensions and the optional custom folder
            extensions = rule_config.get("extensions", [])
            custom_folder_name = rule_config.get("folder", "").strip()
            
            # Determine target path based on whether 'folder' is set
            if custom_folder_name:
                # Target: root destination / custom folder name
                dest_path = Path(destination) / custom_folder_name
            else:
                # Target: root destination / rule name (fallback original behavior)
                dest_path = Path(destination) / rule_name

            # If target folder doesn't exist, prompt the user for creation confirmation
            if not dest_path.exists():
                reply = warning(
                    None, 
                    "Create Folder?", 
                    f"The destination folder structure does not exist:\n'{dest_path}'\n\nWould you like to create it?", 
                    QMessageBox.Yes | QMessageBox.No, 
                    QMessageBox.Yes
                )
                if reply == QMessageBox.Yes:
                    dest_path.mkdir(parents=True, exist_ok=True)
                else:
                    return [] # Abort organizing if they say no

            # Filter and process the files
            extensions_lower = [ext.lower() for ext in extensions]
            moved_files: list[str] = []
    
            for file in source_path.iterdir():
                if file.is_file() and file.suffix.lower() in extensions_lower:
                    dst_file = dest_path / file.name
    
                    try:
                        move(str(file), str(dst_file))
                        moved_files.append(file.name)
                    except Exception as e:
                        error(
                            None,
                            "Error",
                            f"Failed to move file '{file.name}': {e}"
                        )
    
            return moved_files
    
        except Exception as e:
            error(None, "Error", f"Failed to organize files: {e}")
            return []