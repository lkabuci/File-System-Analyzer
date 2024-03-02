import os
from pathlib import Path
from typing import List, Set, Union

from pydantic import BaseModel
from rich import print
from rich.table import Table

from analyzer.AnalyzerInterface import AnalyserInterface
from analyzer.utils.permissions import (
    PermissionType,
    generate_full_write_combination,
    get_file_permissions,
)


class FilePermission(BaseModel):
    file_path: Union[Path, str]
    permissions: PermissionType


class FilePermissionsChecker(AnalyserInterface):
    COLOR_HEADER = "bold magenta"
    COLOR_FILE = "blue"
    COLOR_PERMISSION = "green"

    def __init__(self) -> None:
        """
        Initialize the FilePermissionsChecker.
        """
        self.bad_permissions: Set[PermissionType] = generate_full_write_combination()
        _other_bad_permissions: List[PermissionType] = [
            PermissionType(permission="---------"),  # No permissions
            PermissionType(permission="rwxrwxrwx"),  # Full permissions
            PermissionType(permission="--x--x--x"),  # Execute only
            PermissionType(permission="r-xr-xr-x"),  # Read and execute
        ]
        for permission in _other_bad_permissions:
            self.bad_permissions.add(permission)

        self._table = Table(
            title="Permission Report",
            show_header=True,
            header_style=self.COLOR_HEADER,
            show_edge=True,
        )
        self._table.add_column(
            header="File",
            style=self.COLOR_FILE,
            justify="left",
            vertical="middle",
            overflow="fold",
            no_wrap=False,
        )
        self._table.add_column(
            header="Permissions",
            style=self.COLOR_PERMISSION,
            justify="center",
            vertical="middle",
            no_wrap=False,
        )

    def add(self, file_path) -> None:
        """
        Check the permissions of a file and add it to the reported files if the
        permissions are bad.

        Parameters:
        - file_path (Path): Path to the file.
        """
        try:
            file_permission: PermissionType = get_file_permissions(file_path)
            if file_permission not in self.bad_permissions:
                return
            self._table.add_row(str(file_path), file_permission.permission)
        except (FileNotFoundError, OSError):
            pass

    def report(self) -> None:
        """
        Print the report of files with bad permissions using the rich library.
        """
        if self._table.rows:
            print(self._table)
            return
        print("No files with bad permissions found.")

    def is_report_empty(self) -> bool:
        """
        Check if the permission report is empty.

        Returns:
        - bool: True if the report is empty, False otherwise.
        """
        return not self._table.rows

    def delete_reported_files(self) -> None:
        """
        Delete the files reported as having bad permissions.

        Prints success or error messages for each deletion.
        """
        for file_path in self._table.columns[0]._cells:
            self._delete_file(file_path)

    def _delete_file(self, file_path: Union[Path, str]) -> None:
        """
        Delete a file.
        """
        try:
            os.remove(file_path)
            print(f"[green]Deleted:[/green] {file_path}")
        except Exception as e:
            print(f"[red]Error deleting file {file_path}:[/red] {e}")
