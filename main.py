"""
Application entry point.

Constructs the Model, View, and Controller in the correct order,
then starts the Qt event loop.
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from src.controllers.main_controller import MainController
from src.models.app_model import AppModel
from src.views.main_window_view import MainWindow


def main() -> None:

    # Constants
    ROOT_DIR = Path(__file__).parent
    ASSETS_DIR = ROOT_DIR / "assets"
    STYLES_DIR = ASSETS_DIR / "styles"
    RULES_DIR = ROOT_DIR / "rules"

    # App specific variables
    app_name: str = "FolderMaster"
    org_name: str = "Jovan"
    
    app = QApplication(sys.argv)
    app.setApplicationName(app_name)
    app.setOrganizationName(org_name)

    # Establish Global Layout Theme Skin Configurations
    #default_style = STYLES_DIR / "default.qss"

    #if default_style.is_file and default_style.exists():
    #    with open(default_style, "r", encoding="utf-8") as stream:
    #        app.setStyleSheet(stream.read())

    model = AppModel()
    view = MainWindow(app_name, org_name)
    controller = MainController(view, model)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()