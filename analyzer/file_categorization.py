import os
from collections import defaultdict
from pathlib import Path

from bitmath import NIST, Byte
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

from .directory_traversal import walk_through_dir

# def _get_category(file_extension: str) -> str:
#     }
#
#     for category, extensions in category_mapping.items():
#         if file_extension.lower() in extensions:
#             return category
#     return "Other"


class FileCategorization:
    category_mapping = {
        "image": [
            ".jpg",
            ".jpeg",
            ".jfif",
            ".pjpeg",
            ".pjp",
            ".png",
            ".gif",
            ".webp",
            ".svg",
            ".apng",
            ".avif",
        ],
        "audio": [
            ".3ga",
            ".aac",
            ".ac3",
            ".aif",
            ".aiff",
            ".alac",
            ".amr",
            ".ape",
            ".au",
            ".dss",
            ".flac",
            ".flv",
            ".m4a",
            ".m4b",
            ".m4p",
            ".mp3",
            ".mpga",
            ".ogg",
            ".oga",
            ".mogg",
            ".opus",
            ".qcp",
            ".tta",
            ".voc",
            ".wav",
            ".wma",
            ".wv",
        ],
        "video": [
            ".webm",
            ".MTS",
            ".M2TS",
            ".TS",
            ".mov",
            ".mp4",
            ".m4p",
            ".m4v",
            ".mxf",
        ],
        "text": [".txt", ".md"],
        "code": [
            ".py",
            ".java",
            ".cpp",
            ".html",
            ".css",
            ".js",
            ".sh",
            ".bash",
            ".zsh",
            ".json",
            ".yaml",
            ".xml",
            ".go",
            ".rs",
            ".R",
            ".r",
            ".php",
            ".sql",
            ".pl",
            ".swift",
            ".kt",
            ".kts",
            ".c",
            ".h",
            ".hpp",
            ".cs",
            ".ts",
            ".tsx",
            ".jsx",
            ".rb",
            ".m",
            ".mm",
            ".lua",
            ".dart",
            ".groovy",
            ".scala",
            ".jl",
            ".f90",
            ".f",
        ],
        "linux-related": [
            ".deb",
            ".rpm",
            ".tar",
            ".gz",
            ".zip",
            ".tar.gz",
            ".tar.xz",
            ".bz2",
            ".xz",
            ".sh",
            ".bash",
            ".zsh",
        ],
        "document": [
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".odt",
            ".ods",
            ".odp",
            ".odg",
            ".odf",
            ".odc",
            ".odb",
            ".odm",
            ".ott",
            ".epub",
        ],
    }

    class FileInfo(BaseModel):
        file_path: str
        file_extension: str
        category: str
        size: int

    def __init__(self):
        self.grouped_files = defaultdict(
            lambda: defaultdict(lambda: {"count": 0, "size": 0})
        )
        self.extension_to_category = {
            ext: cat for cat, exts in self.category_mapping.items() for ext in exts
        }
        self.table = Table(title="File Summary")
        self.table.add_column("Category")
        self.table.add_column("File Extension")
        self.table.add_column("Number of Files")
        self.table.add_column("Size")

    def _classify_file(self, filename: Path) -> FileInfo:
        filename_str = str(filename)
        _, file_extension = os.path.splitext(filename_str)
        category = self._get_category(file_extension)
        try:
            size = os.path.getsize(filename_str)
        except FileNotFoundError:
            size = 0
        return self.FileInfo(
            file_path=filename_str,
            file_extension=file_extension,
            category=category,
            size=size,
        )

    def add_file(self, filename: Path) -> None:
        file_info = self._classify_file(filename)
        category = file_info.category
        self.grouped_files[category][file_info.file_extension]["count"] += 1
        self.grouped_files[category][file_info.file_extension]["size"] += file_info.size

    def update_table(self, size_unit: str = "bytes") -> None:
        new_table = Table(title="File Summary")
        new_table.add_column("Category")
        new_table.add_column("File Extension")
        new_table.add_column("Number of Files")
        new_table.add_column("Size")

        last_category = None

        for category, extensions in self.grouped_files.items():
            for extension, file_data in extensions.items():
                size = self._convert_size(file_data["size"], size_unit)

                if last_category is not None and category != last_category:
                    new_table.add_row("", "", "", "")

                new_table.add_row(
                    category if category != last_category else "",
                    extension,
                    str(file_data["count"]),
                    f"{size} {size_unit}",
                )

                last_category = category

        self.table = new_table

    def _convert_size(self, size: int, target_unit: str) -> str:
        size_in_bytes = Byte(size)
        converted_size = size_in_bytes.best_prefix(system=NIST)
        converted_size_str = "{:.2f} {}".format(converted_size.value, target_unit)
        return converted_size_str

    def _get_category(self, file_extension: str) -> str:
        for category, extensions in self.category_mapping.items():
            if file_extension.lower() in extensions:
                return category
        return "Other"

    def display_summary(self, size_unit: str = "bytes") -> None:
        console = Console()
        self.update_table(size_unit=size_unit)
        console.print(self.table)
