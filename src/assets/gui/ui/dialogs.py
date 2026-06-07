from PySide6.QtWidgets import QMessageBox, QWidget


def warning(parent: QWidget | None, title: str, message: str) -> None:
    QMessageBox.warning(parent, title, message)


def info(parent: QWidget | None, title: str, message: str) -> None:
    QMessageBox.information(parent, title, message)


def error(parent: QWidget | None, title: str, message: str) -> None:
    QMessageBox.critical(parent, title, message)