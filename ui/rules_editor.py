"""
ui/rules_editor.py - Rules editor: view, add, delete file sorting rules
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QComboBox, QDialog,
    QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from core.scanner import DEFAULT_RULES


class AddRuleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Rule")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)

        layout.addWidget(QLabel("File Extension  (e.g.  .pdf  or  .jpg)"))
        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText(".ext")
        self.ext_input.setFixedHeight(40)
        layout.addWidget(self.ext_input)

        layout.addWidget(QLabel("Destination Subfolder"))
        self.dest_input = QLineEdit()
        self.dest_input.setPlaceholderText("Documents/PDFs/")
        self.dest_input.setFixedHeight(40)
        layout.addWidget(self.dest_input)

        layout.addWidget(QLabel("Category"))
        self.cat_combo = QComboBox()
        self.cat_combo.setFixedHeight(40)
        self.cat_combo.addItems([
            "Documents", "Images", "Videos", "Music",
            "Archives", "Code", "Programs", "Others"
        ])
        layout.addWidget(self.cat_combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_rule(self):
        return {
            "ext": self.ext_input.text().strip().lower(),
            "dest": self.dest_input.text().strip(),
            "category": self.cat_combo.currentText()
        }


class RulesEditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self._load_defaults()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)

        # Header
        header = QHBoxLayout()
        title = QLabel("Rules Editor")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.addWidget(title)

        sub = QLabel("Define how files are sorted by extension")
        sub.setObjectName("cardSub")
        header.addWidget(sub)
        header.addStretch()

        add_btn = QPushButton("＋  Add Rule")
        add_btn.setObjectName("primaryButton")
        add_btn.setFixedHeight(40)
        add_btn.clicked.connect(self._add_rule)
        header.addWidget(add_btn)

        reset_btn = QPushButton("↺  Reset Defaults")
        reset_btn.setObjectName("secondaryButton")
        reset_btn.setFixedHeight(40)
        reset_btn.clicked.connect(self._reset_defaults)
        header.addWidget(reset_btn)
        layout.addLayout(header)

        # Table card
        frame = QFrame()
        frame.setObjectName("card")
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(20, 16, 20, 16)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Extension", "→ Destination", "Category", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 110)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 100)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(380)
        fl.addWidget(self.table)

        self.rule_count_label = QLabel("")
        self.rule_count_label.setObjectName("cardSub")
        fl.addWidget(self.rule_count_label)
        layout.addWidget(frame)

    def _load_defaults(self):
        self.table.setRowCount(0)
        for ext, dest in DEFAULT_RULES.items():
            cat = self._infer_category(dest)
            self._add_row(ext, dest, cat)
        self._update_count()

    def _infer_category(self, dest: str) -> str:
        d = dest.lower()
        if "image" in d or "photo" in d or "screenshot" in d:
            return "Images"
        if "video" in d:
            return "Videos"
        if "music" in d or "audio" in d:
            return "Music"
        if "document" in d or "pdf" in d or "word" in d or "excel" in d:
            return "Documents"
        if "archive" in d:
            return "Archives"
        if "code" in d or "python" in d or "js" in d or "web" in d:
            return "Code"
        if "program" in d:
            return "Programs"
        return "Others"

    def _add_row(self, ext: str, dest: str, cat: str):
        row = self.table.rowCount()
        self.table.insertRow(row)

        ext_item = QTableWidgetItem(ext)
        ext_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, 0, ext_item)
        self.table.setItem(row, 1, QTableWidgetItem(dest))
        cat_item = QTableWidgetItem(cat)
        cat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, 2, cat_item)

        del_btn = QPushButton("🗑️")
        del_btn.setObjectName("dangerButton")
        del_btn.setFixedSize(60, 30)
        del_btn.clicked.connect(lambda _, r=row: self._delete_row(r))
        self.table.setCellWidget(row, 3, del_btn)
        self.table.setRowHeight(row, 38)

    def _delete_row(self, row: int):
        self.table.removeRow(row)
        self._update_count()

    def _add_rule(self):
        dialog = AddRuleDialog(self)
        if dialog.exec():
            rule = dialog.get_rule()
            if not rule["ext"]:
                QMessageBox.warning(self, "Invalid", "Extension cannot be empty.")
                return
            if not rule["ext"].startswith("."):
                rule["ext"] = "." + rule["ext"]
            self._add_row(rule["ext"], rule["dest"] or "Others/", rule["category"])
            self._update_count()

    def _reset_defaults(self):
        reply = QMessageBox.question(
            self, "Reset",
            "Reset all rules to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._load_defaults()

    def _update_count(self):
        count = self.table.rowCount()
        self.rule_count_label.setText(f"{count} rule{'s' if count != 1 else ''} defined")

    def get_rules(self) -> dict:
        """Return current rules as a dict for use by scanner."""
        rules = {}
        for row in range(self.table.rowCount()):
            ext = self.table.item(row, 0)
            dest = self.table.item(row, 1)
            if ext and dest:
                rules[ext.text()] = dest.text()
        return rules
