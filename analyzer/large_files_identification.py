from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel
from rich import console, print
from rich.prompt import Confirm
from rich.table import Table


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

    def add_file(self, file_path: Path) -> None:
        try:
            size = file_path.stat().st_size
            if size > self.size_threshold:
                entry = self.FileEntry(file_path=file_path, size=size)
                self.large_files.append(entry)
        except FileNotFoundError:
            print(f"[red]File not found:[/red] {file_path}")

    def scan_and_report(self) -> None:
        if not self.large_files:
            print("[green]No large files found.[/green]")
            return

        table = Table(title="Large Files")
        table.add_column("File Path", style="cyan", no_wrap=True)
        table.add_column("Size (bytes)", style="magenta")

        for entry in self.large_files:
            table.add_row(str(entry.file_path), str(entry.size))

        print(table)

        # Ask the user if they want to delete the reported files
        confirm = Confirm.ask("Do you want to delete the reported files?")
        if confirm:
            self.delete_reported_files()

    def delete_reported_files(self) -> None:
        for entry in self.large_files:
            try:
                entry.file_path.unlink()
                print(f"[green]Deleted:[/green] {entry.file_path}")
            except Exception as e:
                print(f"[red]Error deleting file {entry.file_path}:[/red] {e}")
