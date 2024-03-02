import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Union

import bitmath
from pydantic import BaseModel
from rich import box, print
from rich.table import Table

from analyzer.AnalyzerInterface import AnalyserInterface


class FileInfo(BaseModel):
    filename: Union[Path, str]
    extension: str
    category: str
    size: int


class CategoryInfo(BaseModel):
    name: str
    number_of_files: int
    total_size: int
    files: List[FileInfo]


"""
this is an example of CategoryInfo
[
    (
        'Text',               <--- key: category
        CategoryInfo(         <--- value: CategoryInfo
            name='Other',
            number_of_files=1,
            total_size=0,
            files=[FileInfo(
                filename=PosixPath('/tmp.txt'),
                extension='.txt',
                category='Text',
                size=0)       <--- size in Bytes
            ]
        )
    ),
    (
        'Video',
        CategoryInfo(
            name='Other',
            number_of_files=1,
            total_size=0,
            files=[FileInfo(
                filename=PosixPath('/video.mp4'),
                extension='.mp4',
                category='Video',
                size=0)
            ]
        )
    ),
]
"""


file_path = "config/category.json"
category_mapping = Dict[str, List[str]]
try:
    with open(file_path, "r") as file:
        category_mapping = json.load(file)
except Exception as e:
    print(f"[red]Error reading category file: due to {e}[/red]", file=sys.stderr)
    raise SystemExit(1)


class Categorization(AnalyserInterface):

    def __init__(self) -> None:
        self.category_data = defaultdict(
            lambda: CategoryInfo(
                name="Other", number_of_files=0, total_size=0, files=[]
            )
        )

    def add(self, filename: Path) -> None:
        """
        Add a file to the categorized files.

        Parameters:
        - filename (Path): Path to the file.
        """

        extension = filename.suffix
        category = next(
            (
                category
                for category, extensions in category_mapping.items()
                if extension.lower() in extensions
            ),
            "Other",
        )
        try:
            size = filename.stat().st_size
        except FileNotFoundError:
            return

        self.category_data[category].number_of_files += 1
        self.category_data[category].total_size += size
        self.category_data[category].files.append(
            FileInfo(
                filename=filename, extension=extension, category=category, size=size
            )
        )

    def report(self) -> None:
        """
        Display the categorized file summary
        """
        table: Table = Table(
            title="File Summary",
            box=box.HEAVY_EDGE,
            show_lines=True,
            title_style="bold magenta",
        )

        table.add_column(
            "Category", justify="center", vertical="middle", style="bold cyan"
        )
        table.add_column(
            "File Extension", justify="center", vertical="middle", style="italic"
        )
        table.add_column(
            "Number of files", justify="center", vertical="middle", style="bold magenta"
        )
        table.add_column(
            "Size", justify="center", vertical="middle", style="bold magenta"
        )

        bitmath.format_string = "{value:.2f} {unit}"

        for category, category_info in self.category_data.items():
            table.add_row(
                category,
                "\n".join(
                    set(file_info.extension for file_info in category_info.files)
                ),
                str(category_info.number_of_files),
                str(bitmath.Byte(category_info.total_size).best_prefix(bitmath.SI)),
            )
        if not table.rows:
            print("[magneta]No files to categorize.[/magneta]")
            return

        print(table)
