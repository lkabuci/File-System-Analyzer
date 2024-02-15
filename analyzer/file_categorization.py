import os
from collections import defaultdict

from rich.console import Console
from rich.table import Table

from .directory_traversal import walk_through_dir


class FileCategorization:
    def __init__(self):
        self.categories = {}
        self.total_files = 0
        self.total_size = 0
        self.grouped_files = defaultdict(lambda: defaultdict(int))
        self.table = Table(title="File Summary")
        self.table.add_column("Category")
        self.table.add_column("File Extension")
        self.table.add_column("Number of files")
        self.table.add_column("Size")

    def _get_category(self, file_extension):
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
                ".odf",
                ".odm",
                ".ott",
                ".ots",
                ".otp",
                ".otg",
                ".otc",
                ".otf",
                ".oti",
                ".otm",
                ".txt",
                ".rtf",
                ".tex",
                ".csv",
                ".tsv",
                ".json",
                ".yaml",
                ".xml",
                ".html",
                ".htm",
                ".xhtml",
                ".epub",
                ".mobi",
                ".azw",
                ".azw3",
                ".azw4",
                ".azw8",
                ".fb2",
                ".lit",
                ".prc",
                ".pdb",
                ".pml",
                ".rb",
                ".snb",
                ".tcr",
                ".txtz",
                ".cbr",
                ".cbz",
                ".cb7",
                ".cbt",
                ".cba",
                ".djvu",
                ".djv",
                ".doc",
                ".docx",
                ".odt",
                ".pdf",
                ".rtf",
                ".txt",
                ".xls",
                ".xlsx",
                ".ods",
                ".odp",
                ".ppt",
                ".pptx",
                ".odg",
                ".odf",
                ".odc",
                ".odb",
                ".odf",
                ".odm",
                ".ott",
                ".ots",
                ".otp",
                ".otg",
                ".otc",
                ".otf",
                ".oti",
                ".otm",
                ".txt",
                ".rtf",
                ".tex",
                ".csv",
                ".tsv",
                ".json",
                ".yaml",
                ".xml",
                ".html",
                ".htm",
                ".xhtml",
                ".epub",
                ".mobi",
                ".azw",
                ".azw3",
                ".azw4",
                ".azw8",
                ".fb2",
                ".lit",
                ".prc",
                ".pdb",
                ".pml",
                ".rb",
                ".snb",
                ".tcr",
                ".txtz",
                ".cbr",
                ".cbz",
                ".cb7",
                ".cbt",
                ".cba",
                ".djvu",
                ".djv",
                ".doc",
                ".docx",
                ".odt",
                ".pdf",
                ".rtf",
                ".txt",
                ".xls",
                ".xlsx",
                ".ods",
                ".odp",
                ".ppt",
                ".pptx",
                ".odg",
                ".odf",
                ".odc",
                ".odb",
                ".odf",
                ".odm",
                ".ott",
                ".ots",
                ".otp",
            ],
        }

        for category, extensions in category_mapping.items():
            if file_extension.lower() in extensions:
                return category
        return "Other"

    def _classify_file(self, filename):
        filename_str = str(filename)
        _, file_extension = os.path.splitext(filename_str)
        category = self._get_category(file_extension)
        return {
            "file_path": filename_str,
            "file_extension": file_extension,
            "category": category,
            "size": os.path.getsize(filename_str),  # Retrieve the file size
        }

    def add_file(self, filename):
        file_info = self._classify_file(filename)

        # Update the grouped files and total size
        self.grouped_files[file_info["category"]][file_info["file_extension"]] += 1
        self.total_size += file_info["size"]

    def update_table(self):
        # Create a new table
        new_table = Table(title="File Summary")
        new_table.add_column("Category")
        new_table.add_column("File Extension")
        new_table.add_column("Number of files")
        new_table.add_column("Size")

        # Keep track of the last category to add borders
        last_category = None

        # Update the summary table based on grouped files
        for category, extensions in self.grouped_files.items():
            for extension, count in extensions.items():
                size = sum(
                    self._classify_file(filename)["size"]
                    for filename in walk_through_dir(".")
                    if self._get_category(os.path.splitext(filename)[1]) == category
                    and os.path.splitext(filename)[1] == extension
                )

                # Add a border only when the category changes
                if last_category is not None and category != last_category:
                    new_table.add_row("", "", "", "")

                new_table.add_row(
                    (
                        category if category != last_category else ""
                    ),  # Only display category if it changes
                    extension,
                    str(count),
                    f"{size} bytes",
                )

                last_category = category

        # Assign the new table to the existing one
        self.table = new_table

    def display_summary(self):
        console = Console()
        self.update_table()
        console.print(self.table)
