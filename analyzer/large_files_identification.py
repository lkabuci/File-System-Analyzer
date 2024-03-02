from bisect import insort_left
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

import bitmath
from rich import box, print
from rich.prompt import Prompt
from rich.table import Table


@dataclass
class FileEntry:
    file_path: Path
    size: bitmath.Byte


PathLike = Union[Path, str]


class LargeFileIdentifier:
    DEFAULT_THRESHOLD = bitmath.MiB(1)

    def __init__(self, size_threshold: Optional[str] = None):
        """
        Initialize the LargeFileIdentifier.

        Parameters: - size_threshold (Optional[str]): Threshold for identifying large
        files, in a human-readable string format (e.g., "100MB", "2 GiB").
        """
        self.size_threshold = (
            bitmath.parse_string(size_threshold)
            if size_threshold
            else self.DEFAULT_THRESHOLD
        )
        self.large_files: List[FileEntry] = []

    def _parse_size_threshold(self, size_threshold: Optional[str] = None):
        """
        Parses the size threshold from a human-readable string to bitmath.Byte.

        Args: size_threshold (Optional[str]): Threshold for identifying large files,
        in a human-readable string format.

        Returns:
            bitmath.Byte: The parsed size threshold.
        """
        if size_threshold is None:
            return self.DEFAULT_THRESHOLD
        try:
            return bitmath.parse_string(size_threshold)
        except ValueError as e:
            raise ValueError(f"Invalid size threshold format: {e}")

    def add_file(self, file_path: PathLike) -> None:
        """
        Add a file to the list of large files if its size exceeds the threshold.

        Parameters:
            - file_path (Path): Path to the file.
        """
        try:
            size_in_bytes = Path(file_path).stat().st_size
            size = bitmath.Byte(size_in_bytes).best_prefix(bitmath.SI)
            if size >= self.size_threshold:
                file_entry = FileEntry(file_path=file_path, size=size)
                insort_left(self.large_files, file_entry, key=lambda x: x.size)
        except (FileNotFoundError, OSError):
            pass

    def report_large_files(self) -> None:
        """
        Scan for large files and print a report.

        Parameters:
        - size_unit (str): Target unit for file sizes (default is "bytes").
        """
        if not self.large_files:
            print("[green]No large files found.[/green]")
            return

        table = Table(title="Large Files", box=box.HEAVY_EDGE)
        table.add_column("File Path", style="cyan", no_wrap=False)
        table.add_column("Size", style="magenta")
        bitmath.format_string = "{value:.2f} {unit}"

        for entry in self.large_files:
            table.add_row(str(entry.file_path), f"[magenta]{entry.size}[/magenta]")

        print(table)

    def delete_reported_files(self) -> None:
        """
        Delete the files reported as large.

        Prints success or error messages for each deletion.
        """
        for entry in self.large_files:
            try:
                entry.file_path.unlink()
                print(f"[green]Deleted:[/green] [cyan]{entry.file_path}[/cyan]")
            except Exception as e:
                print(f"[red]Error deleting file {entry.file_path}:[/red] {e}")

    def delete_one_file_at_a_time(self) -> None:
        """
        Delete the files reported as large. one by one
        """
        for entry in self.large_files:
            try:
                response = Prompt.ask(
                    f"[red]analyzer: [/red]"
                    f"sure do you want to delete {entry.file_path}",
                    choices=["y", "N"],
                    default="n",
                )
                if response.lower() != "y":
                    continue
                entry.file_path.unlink()
                print(f"[green]Deleted:[/green] [cyan]{entry.file_path}[/cyan]")
            except Exception as e:
                print(f"[red]Error deleting file {entry.file_path}:[/red] {e}")
