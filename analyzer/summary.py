import time
from os import stat
from pathlib import Path
from typing import Union

import bitmath
import rich


class FileStatisticsCollector:
    total_files: int = 0
    total_size: int = 0
    average_size: float = 0.0
    smallest_file_size: float = float("inf")
    largest_file_size: float = 0.0
    start_time: float = time.time()
    report_key_len: int = len("Smallest File Size:   ")

    def add_file(self, file_path: Path) -> None:
        try:
            file_size = stat(file_path).st_size
        except (FileNotFoundError, OSError):
            return

        self.total_files += 1
        self.total_size += file_size

        self.smallest_file_size = min(self.smallest_file_size, file_size)
        self.largest_file_size = max(self.largest_file_size, file_size)

    def _format_size_line(self, key: str, value: Union[int, float]) -> str:
        formatted_value = bitmath.Byte(value).best_prefix(bitmath.SI)
        return f"{key.ljust(self.report_key_len)} {formatted_value}"

    def report_statistics(self) -> None:
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        if self.total_files == 0:
            return
        self.average_size = self.total_size / self.total_files
        bitmath.format_string = "{value:.2f} {unit}"

        rich.print("\n[bold][underline]Statistics[/underline][/bold]")
        rich.print(f"{'Total Files:':<{self.report_key_len}} {self.total_files} file")
        rich.print(self._format_size_line("Total Size:", self.total_size))
        rich.print(self._format_size_line("Average File Size:", self.average_size))
        rich.print(
            self._format_size_line("Smallest File Size:", self.smallest_file_size)
        )
        rich.print(self._format_size_line("Largest File Size:", self.largest_file_size))
        rich.print(
            f"{'Time Elapsed:':<{self.report_key_len}} {elapsed_time:.2f} seconds"
        )
