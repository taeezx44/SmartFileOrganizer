DARK_STYLE = """
QMainWindow, QWidget {
    background-color: #1a1d23;
    color: #e2e8f0;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}
QFrame#sidebar {
    background-color: #13151a;
    border-right: 1px solid #2d3748;
}
QLabel#logoLabel {
    color: #7c3aed;
    padding: 4px 0;
}
QLabel#versionLabel {
    color: #4a5568;
    font-size: 11px;
}
QPushButton#navButton {
    background: transparent;
    color: #a0aec0;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 0 12px;
    font-size: 13px;
}
QPushButton#navButton:hover {
    background-color: #2d3748;
    color: #e2e8f0;
}
QPushButton#navButton:checked {
    background-color: #7c3aed;
    color: #ffffff;
    font-weight: bold;
}
QPushButton#themeButton {
    background-color: #2d3748;
    color: #a0aec0;
    border: none;
    border-radius: 8px;
    padding: 0 12px;
    font-size: 12px;
}
QPushButton#themeButton:hover { background-color: #4a5568; }
QPushButton#primaryButton {
    background-color: #7c3aed;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton#primaryButton:hover { background-color: #6d28d9; }
QPushButton#primaryButton:disabled { background-color: #4a5568; color: #718096; }
QPushButton#dangerButton {
    background-color: #e53e3e;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton#dangerButton:hover { background-color: #c53030; }
QPushButton#secondaryButton {
    background-color: #2d3748;
    color: #e2e8f0;
    border: 1px solid #4a5568;
    border-radius: 8px;
    padding: 10px 20px;
}
QPushButton#secondaryButton:hover { background-color: #4a5568; }
QPushButton#secondaryButton:disabled { background-color: #1e2330; color: #4a5568; }
QFrame#card {
    background-color: #1e2330;
    border: 1px solid #2d3748;
    border-radius: 12px;
}
QLabel#cardTitle { font-size: 14px; font-weight: bold; color: #e2e8f0; }
QLabel#cardValue { font-size: 26px; font-weight: bold; color: #7c3aed; }
QLabel#cardSub { font-size: 11px; color: #718096; }
QLabel#sectionTitle { font-size: 12px; color: #718096; font-weight: bold; text-transform: uppercase; }
QLineEdit, QComboBox {
    background-color: #2d3748;
    color: #e2e8f0;
    border: 1px solid #4a5568;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
}
QLineEdit:focus, QComboBox:focus { border: 1px solid #7c3aed; }
QComboBox::drop-down { border: none; padding-right: 8px; }
QTableWidget {
    background-color: #1e2330;
    color: #e2e8f0;
    border: 1px solid #2d3748;
    border-radius: 8px;
    gridline-color: #2d3748;
    alternate-background-color: #232737;
}
QTableWidget::item { padding: 6px; }
QTableWidget::item:selected { background-color: #7c3aed; color: white; }
QHeaderView::section {
    background-color: #13151a;
    color: #a0aec0;
    border: none;
    border-bottom: 1px solid #2d3748;
    padding: 8px 12px;
    font-weight: bold;
    font-size: 12px;
}
QScrollBar:vertical {
    background: #1a1d23;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical { background: #4a5568; border-radius: 4px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #7c3aed; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QProgressBar {
    background-color: #2d3748;
    border: none;
    border-radius: 4px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk { background-color: #7c3aed; border-radius: 4px; }
QDialog {
    background-color: #1a1d23;
    color: #e2e8f0;
}
QDialogButtonBox QPushButton {
    background-color: #2d3748;
    color: #e2e8f0;
    border: 1px solid #4a5568;
    border-radius: 6px;
    padding: 8px 20px;
    min-width: 80px;
}
QDialogButtonBox QPushButton:hover { background-color: #7c3aed; color: white; border: none; }
"""

LIGHT_STYLE = """
QMainWindow, QWidget {
    background-color: #f7f8fc;
    color: #1a202c;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}
QFrame#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}
QLabel#logoLabel { color: #6d28d9; padding: 4px 0; }
QLabel#versionLabel { color: #a0aec0; font-size: 11px; }
QPushButton#navButton {
    background: transparent;
    color: #4a5568;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 0 12px;
    font-size: 13px;
}
QPushButton#navButton:hover { background-color: #edf2f7; color: #1a202c; }
QPushButton#navButton:checked { background-color: #6d28d9; color: #ffffff; font-weight: bold; }
QPushButton#themeButton { background-color: #edf2f7; color: #4a5568; border: none; border-radius: 8px; padding: 0 12px; font-size: 12px; }
QPushButton#primaryButton { background-color: #6d28d9; color: white; border: none; border-radius: 8px; padding: 10px 20px; font-weight: bold; }
QPushButton#primaryButton:hover { background-color: #5b21b6; }
QPushButton#primaryButton:disabled { background-color: #cbd5e0; color: #a0aec0; }
QPushButton#dangerButton { background-color: #e53e3e; color: white; border: none; border-radius: 8px; padding: 8px 16px; font-weight: bold; }
QPushButton#secondaryButton { background-color: #edf2f7; color: #1a202c; border: 1px solid #cbd5e0; border-radius: 8px; padding: 10px 20px; }
QPushButton#secondaryButton:hover { background-color: #e2e8f0; }
QPushButton#secondaryButton:disabled { background-color: #f7f8fc; color: #a0aec0; }
QFrame#card { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
QLabel#cardTitle { font-size: 14px; font-weight: bold; color: #1a202c; }
QLabel#cardValue { font-size: 26px; font-weight: bold; color: #6d28d9; }
QLabel#cardSub { font-size: 11px; color: #a0aec0; }
QLabel#sectionTitle { font-size: 12px; color: #a0aec0; font-weight: bold; }
QLineEdit, QComboBox { background-color: #ffffff; color: #1a202c; border: 1px solid #cbd5e0; border-radius: 6px; padding: 8px 12px; }
QLineEdit:focus, QComboBox:focus { border: 1px solid #6d28d9; }
QComboBox::drop-down { border: none; padding-right: 8px; }
QTableWidget { background-color: #ffffff; color: #1a202c; border: 1px solid #e2e8f0; border-radius: 8px; gridline-color: #e2e8f0; alternate-background-color: #f7f8fc; }
QTableWidget::item { padding: 6px; }
QTableWidget::item:selected { background-color: #6d28d9; color: white; }
QHeaderView::section { background-color: #f7f8fc; color: #4a5568; border: none; border-bottom: 1px solid #e2e8f0; padding: 8px 12px; font-weight: bold; font-size: 12px; }
QScrollBar:vertical { background: #f7f8fc; width: 8px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #cbd5e0; border-radius: 4px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #6d28d9; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QProgressBar { background-color: #e2e8f0; border: none; border-radius: 4px; color: transparent; }
QProgressBar::chunk { background-color: #6d28d9; border-radius: 4px; }
QDialog { background-color: #f7f8fc; color: #1a202c; }
QDialogButtonBox QPushButton { background-color: #edf2f7; color: #1a202c; border: 1px solid #cbd5e0; border-radius: 6px; padding: 8px 20px; min-width: 80px; }
QDialogButtonBox QPushButton:hover { background-color: #6d28d9; color: white; border: none; }
"""
