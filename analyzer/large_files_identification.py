from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel
from rich import print
from rich.table import Table


def convert_size(size: int, target_unit: str) -> str:
    units = {"bytes": 0, "KB": 1, "MB": 2, "GB": 3}
    current_unit = units[target_unit]

    for _ in range(units["bytes"], current_unit):
        size /= 1024.0

    return (
        f"{size:.2f} {target_unit}" if current_unit > 0 else f"{size:.0f} {target_unit}"
    )


class LargeFileIdentifier:
    class FileEntry(BaseModel):
        file_path: Path
        size: int

    def __init__(self, size_threshold: Optional[int] = None):
        # Default size threshold is 1 MB
        self.size_threshold = (
            size_threshold if size_threshold is not None else 1024 * 1024
        )
        self.large_files: List[LargeFileIdentifier.FileEntry] = []

    def add_file(
        self,
        file_path: Path,
        size_threshold: Optional[int] = None,
        size_unit: str = "bytes",
    ) -> None:
        try:
            size = file_path.stat().st_size
            if size_threshold is None:
                size_threshold = self.size_threshold
            if size > self.convert_threshold(size_threshold, size_unit):
                entry = self.FileEntry(file_path=file_path, size=size)
                self.large_files.append(entry)
        except FileNotFoundError:
            print(f"[red]File not found:[/red] {file_path}")

    def convert_threshold(
        self, size_threshold: Optional[int], size_unit: str
    ) -> Optional[int]:
        if size_threshold is None:
            return None

        units = {"bytes": 0, "KB": 1, "MB": 2, "GB": 3}
        current_unit = units[size_unit]
        converted_threshold = size_threshold

        for _ in range(units["bytes"], current_unit):
            converted_threshold *= 1024

        return converted_threshold

    def scan_and_report(self, size_unit: str = "bytes") -> None:
        if not self.large_files:
            print("[green]No large files found.[/green]")
            return

        table = Table(title="Large Files")
        table.add_column("File Path", style="cyan", no_wrap=True)
        table.add_column(f"Size ({size_unit})", style="magenta")

        for entry in self.large_files:
            size_formatted = convert_size(entry.size, size_unit)
            table.add_row(str(entry.file_path), size_formatted)

        print(table)

    def delete_reported_files(self) -> None:
        for entry in self.large_files:
            try:
                entry.file_path.unlink()
                print(f"[green]Deleted:[/green] {entry.file_path}")
            except Exception as e:
                print(f"[red]Error deleting file {entry.file_path}:[/red] {e}")
