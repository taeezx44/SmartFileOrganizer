"""
Smart File Organizer Pro - main.py
Entry point
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Smart File Organizer Pro")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SmartOrganizer")
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
