import sys
from pathlib import Path

from bitmath import Byte
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table
from rich.text import Text


class FileStatisticsCollector(BaseModel):
    total_files: int = 0
    total_size: int = 0
    average_size: float = 0
    smallest_file_size: int = sys.maxsize  # Initialize with the maximum possible value
    largest_file_size: int = 0

    def add_file(self, file_path: Path) -> None:
        try:
            file_size = file_path.stat().st_size
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return

        self.total_files += 1
        self.total_size += file_size
        self.average_size = self.total_size / self.total_files

        # Update smallest and largest files
        self.smallest_file_size = min(self.smallest_file_size, file_size)
        self.largest_file_size = max(self.largest_file_size, file_size)

    def report_statistics(self) -> None:
        """
        Print the file statistics report using rich formatting and bitmath for file sizes.

        Returns:
        - None
        """
        console = Console()
        table = Table(
            title=Text("File Statistics Report", style="bold green"),
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="yellow")

        table.add_row("Total Files", str(self.total_files))
        table.add_row(
            "Total Size",
            f"{Byte(self.total_size).to_Byte().best_prefix().value:.2f} MB",
        )
        table.add_row(
            "Average File Size",
            f"{Byte(self.average_size).to_Byte().best_prefix().value:.2f} MB",
        )
        table.add_row(
            "Smallest File Size",
            f"{Byte(self.smallest_file_size).to_Byte().best_prefix().value:.2f} KB",
        )
        table.add_row(
            "Largest File Size",
            f"{Byte(self.largest_file_size).to_Byte().best_prefix().value:.2f} MB",
        )

        console.print(table)
