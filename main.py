"""
Smart File Organizer Pro - main.py
Entry point
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Smart File Organizer Pro")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SmartOrganizer")
    # AA_UseHighDpiPixmaps removed in PyQt6 6.4+ (enabled by default)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
