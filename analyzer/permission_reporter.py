import os
from typing import List

from rich import print
from rich.table import Table


class FilePermissionsChecker:
    def __init__(self) -> None:
        self.reported_files: List[str] = []
        self.bad_permissions: List[str] = [
            "777",  # Full permissions for everyone
            "776",
            "775",
            "774",
            "773",
            "772",
            "771",
            "770",
            "667",
            "666",
            "665",
            "664",
            "663",
            "662",
            "661",
            "660",
            "557",
            "556",
            "555",
            "700",
            "600",
            "444",
            "400",
            "200",
            "100",
            "000",
        ]

    def check_permissions(self, filepath: str) -> None:
        file_stat = os.stat(filepath)
        octal_permissions = oct(file_stat.st_mode)[-3:]
        if octal_permissions in self.bad_permissions:
            self.reported_files.append(filepath)

    def report_permissions(self) -> None:
        """
        Report the permissions of the files in the PermissionReporter's list.

        Prints the file path along with its permissions in rwx format in a table.

        Raises:
            - FileNotFoundError: If a file from the list is not found.
            - Exception: If an unexpected error occurs during processing.
        """
        table = Table(title="Permission Report")
        table.add_column("File", style="blue")
        table.add_column("Permissions", style="green")

        for file_path in self.reported_files:
            try:
                # Get the file permissions as an integer
                permissions = os.stat(file_path).st_mode

                # Convert the integer to a string representation in octal format
                permissions_str = oct(permissions)[-3:]

                # Convert octal permissions to rwx format without list comprehension
                rwx_permissions = ""
                for i in range(0, 3):
                    rwx_permissions += "r" if int(permissions_str[i]) & 4 else "-"
                    rwx_permissions += "w" if int(permissions_str[i]) & 2 else "-"
                    rwx_permissions += "x" if int(permissions_str[i]) & 1 else "-"

                # Add row to the table
                table.add_row(file_path, rwx_permissions)
            except FileNotFoundError:
                # Add row for file not found
                table.add_row(f"[red]{file_path}[/red]", "File not found")
            except Exception as e:
                # Add row for other errors
                table.add_row(
                    f"[red]{file_path}[/red]", f"[bold red]Error: {e}[/bold red]"
                )

        print(table)
