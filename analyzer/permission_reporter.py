import os
from pathlib import Path
from typing import List

from pydantic import BaseModel
from rich import print
from rich.table import Table


class FilePermissionsChecker:
    class FilePermissionReport(BaseModel):
        file_path: Path
        permissions: str

    def __init__(self) -> None:
        self.reported_files: List[Path] = []
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
            "400",
            "200",
            "100",
            "000",
        ]

    def check_permissions(self, file_path: Path) -> None:
        file_stat = os.stat(file_path)
        octal_permissions = oct(file_stat.st_mode)[-3:]
        if octal_permissions in self.bad_permissions:
            self.reported_files.append(file_path)

    def generate_permission_report(self) -> List[FilePermissionReport]:
        reports = []
        for file_path in self.reported_files:
            try:
                permissions_int = os.stat(file_path).st_mode
                permissions_str = oct(permissions_int)[-3:]
                rwx_permissions = self._convert_octal_to_rwx(permissions_str)

                report_entry = self.FilePermissionReport(
                    file_path=file_path, permissions=rwx_permissions
                )

                reports.append(report_entry)
            except FileNotFoundError:
                # Handle file not found exception
                reports.append(
                    self.FilePermissionReport(
                        file_path=file_path, permissions="File not found"
                    )
                )
            except Exception as e:
                # Handle other exceptions
                reports.append(
                    self.FilePermissionReport(
                        file_path=file_path, permissions=f"Error: {e}"
                    )
                )

        return reports

    def print_permission_report(self) -> None:
        reports = self.generate_permission_report()

        if reports:
            table = Table(title="Permission Report")
            table.add_column("File", style="blue")
            table.add_column("Permissions", style="green")

            for report_entry in reports:
                table.add_row(str(report_entry.file_path), report_entry.permissions)

            print(table)
        else:
            print("No files with bad permissions found.")

    def _convert_octal_to_rwx(self, octal_permissions: str) -> str:
        rwx_permissions = ""
        for digit in octal_permissions:
            rwx_permissions += "r" if int(digit) & 4 else "-"
            rwx_permissions += "w" if int(digit) & 2 else "-"
            rwx_permissions += "x" if int(digit) & 1 else "-"
        return rwx_permissions
