"""
core/scanner.py - Scans a directory and returns file info
"""
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List


@dataclass
class FileInfo:
    name: str
    path: str
    extension: str
    size_bytes: int
    destination: str = ""

    @property
    def size_str(self) -> str:
        if self.size_bytes < 1024:
            return f"{self.size_bytes} B"
        elif self.size_bytes < 1024 ** 2:
            return f"{self.size_bytes / 1024:.1f} KB"
        elif self.size_bytes < 1024 ** 3:
            return f"{self.size_bytes / 1024 ** 2:.1f} MB"
        return f"{self.size_bytes / 1024 ** 3:.1f} GB"


DEFAULT_RULES = {
    ".jpg": "Images/Photos/",
    ".jpeg": "Images/Photos/",
    ".png": "Images/Screenshots/",
    ".gif": "Images/GIFs/",
    ".bmp": "Images/",
    ".webp": "Images/",
    ".svg": "Images/SVG/",
    ".mp4": "Videos/",
    ".mov": "Videos/",
    ".avi": "Videos/",
    ".mkv": "Videos/",
    ".wmv": "Videos/",
    ".mp3": "Music/",
    ".wav": "Music/",
    ".flac": "Music/",
    ".aac": "Music/",
    ".ogg": "Music/",
    ".pdf": "Documents/PDFs/",
    ".doc": "Documents/Word/",
    ".docx": "Documents/Word/",
    ".xls": "Documents/Excel/",
    ".xlsx": "Documents/Excel/",
    ".ppt": "Documents/PowerPoint/",
    ".pptx": "Documents/PowerPoint/",
    ".txt": "Documents/Text/",
    ".csv": "Documents/CSV/",
    ".zip": "Archives/",
    ".rar": "Archives/",
    ".7z": "Archives/",
    ".tar": "Archives/",
    ".gz": "Archives/",
    ".exe": "Programs/",
    ".msi": "Programs/",
    ".py": "Code/Python/",
    ".js": "Code/JavaScript/",
    ".ts": "Code/TypeScript/",
    ".html": "Code/Web/",
    ".css": "Code/Web/",
    ".json": "Code/Config/",
    ".xml": "Code/Config/",
    ".yaml": "Code/Config/",
    ".yml": "Code/Config/",
}


def scan_folder(folder_path: str, rules: dict = None) -> List[FileInfo]:
    """Scan folder and return list of FileInfo with destination assigned."""
    if rules is None:
        rules = DEFAULT_RULES

    result = []
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return result

    for item in folder.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            size = item.stat().st_size
            dest = rules.get(ext, "Others/")
            result.append(FileInfo(
                name=item.name,
                path=str(item),
                extension=ext or "(none)",
                size_bytes=size,
                destination=dest,
            ))

    return sorted(result, key=lambda f: f.extension)
