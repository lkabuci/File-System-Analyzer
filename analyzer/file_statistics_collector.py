import sys
import time
from pathlib import Path

from bitmath import Byte
from rich.console import Console


class FileStatisticsCollector:
    def __init__(self):
        self.total_files = 0
        self.total_size = 0
        self.average_size = 0
        self.smallest_file_size = sys.maxsize
        self.largest_file_size = 0
        self.start_time = time.time()

    def add_file(self, file_path: Path) -> None:
        try:
            file_size = file_path.stat().st_size
        except (FileNotFoundError, OSError):
            return

        self.total_files += 1
        self.total_size += file_size
        self.average_size = self.total_size / self.total_files

        self.smallest_file_size = min(self.smallest_file_size, file_size)
        self.largest_file_size = max(self.largest_file_size, file_size)

    def report_statistics(self) -> None:
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        indent_length = len("Smallest File Size:   ")
        console = Console()
        console.print("[bold green]File Statistics Report[/bold green]")
        console.print("=" * 23)
        console.print("Total Files:".ljust(indent_length) + f"{self.total_files}")
        console.print(
            "Total Size:".ljust(indent_length)
            + f"{Byte(self.total_size).to_Byte().best_prefix().value:.2f} MB"
        )
        console.print(
            "Average File Size:".ljust(indent_length)
            + f"{Byte(self.average_size).to_Byte().best_prefix().value:.2f} MB"
        )
        console.print(
            "Smallest File Size:".ljust(indent_length)
            + f"{Byte(self.smallest_file_size).to_Byte().best_prefix().value:.2f} KB"
        )
        console.print(
            "Largest File Size:".ljust(indent_length)
            + f"{Byte(self.largest_file_size).to_Byte().best_prefix().value:.2f} MB"
        )
        console.print(
            "Time Elapsed:".ljust(indent_length) + f"{elapsed_time:.2f} seconds"
        )
