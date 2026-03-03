"""
ui/dashboard.py - Dashboard page with stats and recent activity
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QGridLayout, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from data import database


def _stat_card(icon: str, title: str, value: str, sub: str) -> QFrame:
    card = QFrame()
    card.setObjectName("card")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(20, 18, 20, 18)
    layout.setSpacing(4)

    QLabel(icon, font=QFont("Segoe UI", 22), parent=card)
    layout.addWidget(QLabel(icon, font=QFont("Segoe UI", 22)))

    t = QLabel(title)
    t.setObjectName("cardTitle")
    layout.addWidget(t)

    v = QLabel(value)
    v.setObjectName("cardValue")
    layout.addWidget(v)

    s = QLabel(sub)
    s.setObjectName("cardSub")
    layout.addWidget(s)

    return card, v   # return card + value label so we can update it


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(24)

        title = QLabel("Dashboard")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # Stat cards
        grid = QGridLayout()
        grid.setSpacing(16)

        self._card_files, self._val_files = self._make_card("📁", "Files Organized", "0", "total files moved")
        self._card_space, self._val_space = self._make_card("💾", "Space Processed", "0 MB", "total data moved")
        self._card_sessions, self._val_sessions = self._make_card("🔄", "Sessions", "0", "organize runs")
        self._card_last, self._val_last = self._make_card("⏱️", "Last Run", "Never", "most recent session")

        grid.addWidget(self._card_files, 0, 0)
        grid.addWidget(self._card_space, 0, 1)
        grid.addWidget(self._card_sessions, 0, 2)
        grid.addWidget(self._card_last, 0, 3)
        layout.addLayout(grid)

        # Recent activity table
        activity_frame = QFrame()
        activity_frame.setObjectName("card")
        af = QVBoxLayout(activity_frame)
        af.setContentsMargins(20, 18, 20, 18)
        af.setSpacing(12)

        act_title = QLabel("📋  Recent Sessions")
        act_title.setObjectName("cardTitle")
        af.addWidget(act_title)

        self.activity_table = QTableWidget(0, 3)
        self.activity_table.setHorizontalHeaderLabels(["Folder", "Files Moved", "Date"])
        self.activity_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.activity_table.setColumnWidth(1, 110)
        self.activity_table.setColumnWidth(2, 160)
        self.activity_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.activity_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.activity_table.setAlternatingRowColors(True)
        self.activity_table.setMaximumHeight(220)
        af.addWidget(self.activity_table)

        layout.addWidget(activity_frame)
        layout.addStretch()

    def _make_card(self, icon, title, value, sub):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(4)

        layout.addWidget(QLabel(icon, font=QFont("Segoe UI", 22)))

        t = QLabel(title)
        t.setObjectName("cardTitle")
        layout.addWidget(t)

        v = QLabel(value)
        v.setObjectName("cardValue")
        layout.addWidget(v)

        s = QLabel(sub)
        s.setObjectName("cardSub")
        layout.addWidget(s)

        return card, v

    def refresh(self):
        try:
            stats = database.get_stats()
            self._val_files.setText(stats.get("total_files", "0"))

            bytes_val = int(stats.get("total_bytes", 0))
            if bytes_val < 1024 ** 2:
                space_str = f"{bytes_val / 1024:.1f} KB"
            elif bytes_val < 1024 ** 3:
                space_str = f"{bytes_val / 1024 ** 2:.1f} MB"
            else:
                space_str = f"{bytes_val / 1024 ** 3:.2f} GB"
            self._val_space.setText(space_str)

            self._val_sessions.setText(stats.get("total_sessions", "0"))
            self._val_last.setText(stats.get("last_run", "Never"))

            sessions = database.get_recent_sessions()
            self.activity_table.setRowCount(0)
            for s in sessions:
                row = self.activity_table.rowCount()
                self.activity_table.insertRow(row)
                self.activity_table.setItem(row, 0, QTableWidgetItem(s["folder"]))
                count_item = QTableWidgetItem(str(s["files_moved"]))
                count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.activity_table.setItem(row, 1, count_item)
                self.activity_table.setItem(row, 2, QTableWidgetItem(s["created_at"][:16]))

        except Exception:
            pass  # DB not initialized yet

    def update_stats(self, stats: dict):
        """Called via signal after organize finishes."""
        self.refresh()
