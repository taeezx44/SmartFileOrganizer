"""
core/undo_manager.py - Undo the last organize operation
"""
import shutil
from pathlib import Path
from typing import List, Tuple
from PyQt6.QtCore import QThread, pyqtSignal


class UndoWorker(QThread):
    """Background thread to undo the last organize session."""
    progress = pyqtSignal(int)
    finished = pyqtSignal(int)   # number of files restored
    error = pyqtSignal(str)

    def __init__(self, moves: List[Tuple[str, str]]):
        super().__init__()
        self.moves = moves   # list of (current_path, original_path)

    def run(self):
        total = len(self.moves)
        restored = 0
        for i, (current, original) in enumerate(self.moves):
            try:
                src = Path(current)
                dst = Path(original)
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    restored += 1
            except Exception as e:
                self.error.emit(f"Undo error: {e}")
            self.progress.emit(int((i + 1) / total * 100))

        # Clean up empty folders left behind
        self._cleanup_empty_dirs()
        self.finished.emit(restored)

    def _cleanup_empty_dirs(self):
        checked = set()
        for current, _ in self.moves:
            folder = Path(current).parent
            for parent in [folder, folder.parent, folder.parent.parent]:
                if str(parent) in checked:
                    continue
                checked.add(str(parent))
                try:
                    if parent.exists() and not any(parent.iterdir()):
                        parent.rmdir()
                except Exception:
                    pass


class UndoManager:
    """Stores the last organize session for undo."""

    def __init__(self):
        self._history: List[List[Tuple[str, str]]] = []
        self._max_sessions = 5

    def push(self, moves: List[Tuple[str, str]]):
        """Store a new session's moves."""
        if moves:
            self._history.append(moves)
            if len(self._history) > self._max_sessions:
                self._history.pop(0)

    def pop(self) -> List[Tuple[str, str]]:
        """Get the last session's moves and remove from history."""
        if self._history:
            return self._history.pop()
        return []

    def can_undo(self) -> bool:
        return bool(self._history)

    def sessions_count(self) -> int:
        return len(self._history)
