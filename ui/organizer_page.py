"""
ui/organizer_page.py - Organizer page: scan, preview, organize, undo
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from core.scanner import scan_folder, FileInfo
from core.sorter import SorterWorker
from core.undo_manager import UndoManager, UndoWorker
from data import database


class OrganizerPageWidget(QWidget):
    stats_updated = pyqtSignal(dict)   # emitted after organize finishes

    def __init__(self):
        super().__init__()
        self.files: list[FileInfo] = []
        self.undo_manager = UndoManager()
        self._worker = None
        self._undo_worker = None
        database.init_db()
        self._build_ui()

    # ------------------------------------------------------------------ #
    #  UI BUILD                                                            #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)

        # Page title
        title = QLabel("Organizer")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # Folder picker card
        layout.addWidget(self._folder_card())

        # Preview table card
        layout.addWidget(self._preview_card())

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setFixedHeight(8)
        layout.addWidget(self.progress)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setObjectName("cardSub")
        layout.addWidget(self.status_label)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.undo_btn = QPushButton("↩️  Undo Last")
        self.undo_btn.setObjectName("secondaryButton")
        self.undo_btn.setFixedHeight(44)
        self.undo_btn.setEnabled(False)
        self.undo_btn.clicked.connect(self._undo)
        btn_row.addWidget(self.undo_btn)

        self.organize_btn = QPushButton("✨  Organize Now")
        self.organize_btn.setObjectName("primaryButton")
        self.organize_btn.setFixedHeight(44)
        self.organize_btn.setMinimumWidth(160)
        self.organize_btn.setEnabled(False)
        self.organize_btn.clicked.connect(self._organize)
        btn_row.addWidget(self.organize_btn)

        layout.addLayout(btn_row)

    def _folder_card(self):
        frame = QFrame()
        frame.setObjectName("card")
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(20, 16, 20, 16)
        fl.setSpacing(10)

        lbl = QLabel("📁  Target Folder")
        lbl.setObjectName("cardTitle")
        fl.addWidget(lbl)

        row = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select a folder to organize...")
        self.folder_input.setFixedHeight(40)
        self.folder_input.textChanged.connect(self._on_folder_changed)
        row.addWidget(self.folder_input)

        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondaryButton")
        browse_btn.setFixedSize(100, 40)
        browse_btn.clicked.connect(self._browse)
        row.addWidget(browse_btn)
        fl.addLayout(row)
        return frame

    def _preview_card(self):
        frame = QFrame()
        frame.setObjectName("card")
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(20, 16, 20, 16)
        fl.setSpacing(10)

        header_row = QHBoxLayout()
        title = QLabel("📋  Preview")
        title.setObjectName("cardTitle")
        header_row.addWidget(title)

        self.file_count_label = QLabel("")
        self.file_count_label.setObjectName("cardSub")
        header_row.addWidget(self.file_count_label)
        header_row.addStretch()

        self.scan_btn = QPushButton("🔍  Scan Folder")
        self.scan_btn.setObjectName("secondaryButton")
        self.scan_btn.setFixedHeight(36)
        self.scan_btn.setEnabled(False)
        self.scan_btn.clicked.connect(self._scan)
        header_row.addWidget(self.scan_btn)
        fl.addLayout(header_row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["File Name", "Type", "Size", "→ Destination"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(1, 90)
        self.table.setColumnWidth(2, 90)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(280)
        fl.addWidget(self.table)
        return frame

    # ------------------------------------------------------------------ #
    #  ACTIONS                                                             #
    # ------------------------------------------------------------------ #
    def _browse(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Organize")
        if folder:
            self.folder_input.setText(folder)

    def _on_folder_changed(self, text):
        valid = os.path.isdir(text)
        self.scan_btn.setEnabled(valid)
        if not valid:
            self.organize_btn.setEnabled(False)

    def _scan(self):
        folder = self.folder_input.text().strip()
        if not folder or not os.path.isdir(folder):
            return

        self.files = scan_folder(folder)
        self.table.setRowCount(0)

        for fi in self.files:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(fi.name))

            ext_item = QTableWidgetItem(fi.extension)
            ext_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, ext_item)

            size_item = QTableWidgetItem(fi.size_str)
            size_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 2, size_item)

            self.table.setItem(row, 3, QTableWidgetItem(fi.destination))

        count = len(self.files)
        self.file_count_label.setText(f"{count} file{'s' if count != 1 else ''} found")
        self.organize_btn.setEnabled(count > 0)
        self.status_label.setText("Ready to organize." if count > 0 else "No files found in folder.")

    def _organize(self):
        folder = self.folder_input.text().strip()
        if not self.files:
            return

        reply = QMessageBox.question(
            self, "Confirm",
            f"Move {len(self.files)} files into categorized subfolders?\n\nFolder: {folder}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self._set_ui_busy(True)
        self._worker = SorterWorker(self.files, folder)
        self._worker.progress.connect(self.progress.setValue)
        self._worker.file_done.connect(lambda name, dest: self.status_label.setText(f"Moving: {name}"))
        self._worker.finished.connect(self._on_organize_done)
        self._worker.error.connect(lambda msg: self.status_label.setText(msg))
        self._worker.start()

    def _on_organize_done(self, moves):
        total_bytes = sum(fi.size_bytes for fi in self.files)
        self.undo_manager.push(moves)
        database.save_session(
            self.folder_input.text().strip(),
            len(moves), total_bytes, moves
        )

        self._set_ui_busy(False)
        self.undo_btn.setEnabled(self.undo_manager.can_undo())
        self.status_label.setText(f"✅  Done! {len(moves)} files organized successfully.")
        self.table.setRowCount(0)
        self.files = []
        self.organize_btn.setEnabled(False)
        self.file_count_label.setText("")

        # Emit stats for dashboard
        self.stats_updated.emit(database.get_stats())

    def _undo(self):
        moves = self.undo_manager.pop()
        if not moves:
            return

        reply = QMessageBox.question(
            self, "Undo",
            f"Restore {len(moves)} files to their original locations?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            self.undo_manager.push(moves)
            return

        self._set_ui_busy(True)
        self._undo_worker = UndoWorker(moves)
        self._undo_worker.progress.connect(self.progress.setValue)
        self._undo_worker.finished.connect(self._on_undo_done)
        self._undo_worker.error.connect(lambda msg: self.status_label.setText(msg))
        self._undo_worker.start()

    def _on_undo_done(self, count):
        self._set_ui_busy(False)
        self.undo_btn.setEnabled(self.undo_manager.can_undo())
        self.status_label.setText(f"↩️  Restored {count} files successfully.")

    def _set_ui_busy(self, busy: bool):
        self.progress.setVisible(busy)
        self.progress.setValue(0)
        self.organize_btn.setEnabled(not busy)
        self.scan_btn.setEnabled(not busy)
        self.undo_btn.setEnabled(not busy)
        self.folder_input.setEnabled(not busy)
