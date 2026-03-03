"""
core/sorter.py - Moves files to destination folders
"""
import os
import shutil
from pathlib import Path
from typing import List, Callable
from PyQt6.QtCore import QThread, pyqtSignal
from core.scanner import FileInfo


class SorterWorker(QThread):
    """Background thread for moving files without freezing the UI."""
    progress = pyqtSignal(int)           # percent 0-100
    file_done = pyqtSignal(str, str)     # (filename, dest)
    finished = pyqtSignal(list)          # list of (src, dst) tuples for undo
    error = pyqtSignal(str)

    def __init__(self, files: List[FileInfo], base_folder: str):
        super().__init__()
        self.files = files
        self.base_folder = base_folder
        self._moved: list = []

    def run(self):
        total = len(self.files)
        if total == 0:
            self.finished.emit([])
            return

        for i, file_info in enumerate(self.files):
            try:
                src = Path(file_info.path)
                if not src.exists():
                    continue

                dest_dir = Path(self.base_folder) / file_info.destination
                dest_dir.mkdir(parents=True, exist_ok=True)

                dest_path = dest_dir / file_info.name

                # Handle duplicate filenames
                if dest_path.exists():
                    stem = src.stem
                    suffix = src.suffix
                    counter = 1
                    while dest_path.exists():
                        dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                shutil.move(str(src), str(dest_path))
                self._moved.append((str(dest_path), str(src)))  # (new_path, original_path)
                self.file_done.emit(file_info.name, str(dest_dir))

            except Exception as e:
                self.error.emit(f"Error moving {file_info.name}: {str(e)}")

            self.progress.emit(int((i + 1) / total * 100))

        self.finished.emit(self._moved)
