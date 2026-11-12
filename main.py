"""
Application entry point.

Constructs the Model, View, and Controller in the correct order,
then starts the Qt event loop.
"""

import logging
import sys
from pathlib import Path

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from src.controllers.main_controller import MainController
from src.models.app_model import AppModel
from src.views.main_window_view import MainWindow

ROOT_DIR = Path(__file__).resolve().parent
STYLES_DIR = ROOT_DIR / "src" / "assets" / "styles"
DEFAULT_STYLE = STYLES_DIR / "default.qss"

APP_NAME = "FolderMaster"
ORG_NAME = "Jovan"


def apply_theme(app: QApplication, qss_file: Path) -> None:
    """Fusion + a matching dark palette keeps native-drawn parts (arrows, dialogs) consistent with the QSS."""
    app.setStyle("Fusion")

    palette = QPalette()
    roles = {
        QPalette.ColorRole.Window: "#16181d",
        QPalette.ColorRole.WindowText: "#e4e6eb",
        QPalette.ColorRole.Base: "#14161a",
        QPalette.ColorRole.AlternateBase: "#181a1f",
        QPalette.ColorRole.Text: "#e4e6eb",
        QPalette.ColorRole.Button: "#252830",
        QPalette.ColorRole.ButtonText: "#e4e6eb",
        QPalette.ColorRole.Highlight: "#26a69a",
        QPalette.ColorRole.HighlightedText: "#ffffff",
        QPalette.ColorRole.ToolTipBase: "#252830",
        QPalette.ColorRole.ToolTipText: "#e4e6eb",
        QPalette.ColorRole.PlaceholderText: "#6f7584",
        QPalette.ColorRole.Link: "#4fc3b6",
    }
    for role, color in roles.items():
        palette.setColor(role, QColor(color))
    for role in (QPalette.ColorRole.WindowText, QPalette.ColorRole.Text, QPalette.ColorRole.ButtonText):
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor("#575d6a"))
    app.setPalette(palette)

    try:
        qss = qss_file.read_text(encoding="utf-8")
    except OSError as e:
        logging.warning("Could not load stylesheet %s: %s", qss_file, e)
        return
    # QSS url() paths are resolved against the CWD, so inject an absolute path to the icons
    app.setStyleSheet(qss.replace("@ICONS@", (qss_file.parent / "icons").as_posix()))


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    apply_theme(app, DEFAULT_STYLE)

    model = AppModel()
    view = MainWindow(APP_NAME, ORG_NAME)
    controller = MainController(view, model)  # noqa: F841  (kept alive for the app's lifetime)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
