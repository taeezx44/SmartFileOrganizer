"""
ui/main_window.py - Main Application Window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.styles import DARK_STYLE, LIGHT_STYLE
from ui.dashboard import DashboardWidget
from ui.rules_editor import RulesEditorWidget
from ui.organizer_page import OrganizerPageWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark = True
        self.setWindowTitle("Smart File Organizer Pro")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 760)
        self._build_ui()
        self.apply_theme()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = self._build_sidebar()
        root.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.organizer_page = OrganizerPageWidget()
        self.dashboard_page = DashboardWidget()
        self.rules_page = RulesEditorWidget()

        self.stack.addWidget(self.organizer_page)   # 0
        self.stack.addWidget(self.dashboard_page)   # 1
        self.stack.addWidget(self.rules_page)       # 2
        root.addWidget(self.stack)

        # Connect organizer signals to dashboard
        self.organizer_page.stats_updated.connect(self.dashboard_page.update_stats)

    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(6)

        logo = QLabel("🗂️  File Organizer")
        logo.setObjectName("logoLabel")
        logo.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(logo)

        ver = QLabel("Pro v1.0")
        ver.setObjectName("versionLabel")
        layout.addWidget(ver)
        layout.addSpacing(24)

        sep = QLabel("NAVIGATION")
        sep.setObjectName("sectionTitle")
        layout.addWidget(sep)
        layout.addSpacing(4)

        self.nav_buttons = []
        for text, idx in [("🏠  Organizer", 0), ("📊  Dashboard", 1), ("⚙️  Rules", 2)]:
            btn = QPushButton(text)
            btn.setObjectName("navButton")
            btn.setCheckable(True)
            btn.setFixedHeight(44)
            btn.clicked.connect(lambda _, i=idx, b=btn: self._nav(i, b))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        self.nav_buttons[0].setChecked(True)
        layout.addStretch()

        self.theme_btn = QPushButton("☀️  Light Mode")
        self.theme_btn.setObjectName("themeButton")
        self.theme_btn.setFixedHeight(38)
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)
        return sidebar

    def _nav(self, index, clicked):
        self.stack.setCurrentIndex(index)
        for b in self.nav_buttons:
            b.setChecked(False)
        clicked.setChecked(True)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()
        self.theme_btn.setText("☀️  Light Mode" if self.is_dark else "🌙  Dark Mode")

    def apply_theme(self):
        self.setStyleSheet(DARK_STYLE if self.is_dark else LIGHT_STYLE)
