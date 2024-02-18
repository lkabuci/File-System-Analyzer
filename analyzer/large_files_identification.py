from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel
from rich import print
from rich.table import Table


def convert_size(size: int, target_unit: str) -> str:
    """
    Convert a given size in bytes to the target unit.

    Parameters:
    - size (int): The size in bytes to be converted.
    - target_unit (str): The unit to which the size should be converted.

    Returns:
    str: A string representation of the size in the target unit.
    """
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
        """
        Initialize the LargeFileIdentifier.

        Parameters:
        - size_threshold (Optional[int]): Threshold for identifying large files, in bytes.
        """
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
        """
        Add a file to the list of large files if its size exceeds the threshold.

        Parameters:
        - file_path (Path): Path to the file.
        - size_threshold (Optional[int]): Threshold for identifying large files, in bytes.
        - size_unit (str): Target unit for size comparison (default is "bytes").
        """
        try:
            size = file_path.stat().st_size
            if size_threshold is None:
                size_threshold = self.size_threshold
            if size > self.convert_threshold(size_threshold, size_unit):
                entry = self.FileEntry(file_path=file_path, size=size)
                self.large_files.append(entry)
        except (FileNotFoundError, OSError):
            pass

    def convert_threshold(
        self, size_threshold: Optional[int], size_unit: str
    ) -> Optional[int]:
        """
        Convert the size threshold to the target unit.

        Parameters:
        - size_threshold (Optional[int]): Threshold for identifying large files, in bytes.
        - size_unit (str): Target unit for conversion.

        Returns:
        Optional[int]: Converted size threshold.
        """
        if size_threshold is None:
            return None

        units = {"bytes": 0, "KB": 1, "MB": 2, "GB": 3}
        current_unit = units[size_unit]
        converted_threshold = size_threshold

        for _ in range(units["bytes"], current_unit):
            converted_threshold *= 1024

        return converted_threshold

    def scan_and_report(self, size_unit: str = "bytes") -> None:
        """
        Scan for large files and print a report.

        Parameters:
        - size_unit (str): Target unit for file sizes (default is "bytes").
        """
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
        """
        Delete the files reported as large.

        Prints success or error messages for each deletion.
        """
        for entry in self.large_files:
            try:
                entry.file_path.unlink()
                print(f"[green]Deleted:[/green] {entry.file_path}")
            except Exception as e:
                print(f"[red]Error deleting file {entry.file_path}:[/red] {e}")
