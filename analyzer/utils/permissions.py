import os
import stat
from pathlib import Path
from typing import Set, Union

from pydantic import BaseModel


class PermissionType(BaseModel):
    permission: str
    # constr(pattern=r"^([r-][w-][x-]){3}$")  # type: ignore # noqa: F722

    # Override the __hash__ method to allow the PermissionType to be used as a key in
    # a set.
    def __hash__(self):
        return hash(self.permission)


def generate_single_write_combination() -> Set[str]:
    write_permission_template = ".w."
    single_write_combination = set()

    for char in write_permission_template:
        if char == "w":
            continue
        for r in ["r", "-"]:
            for x in ["x", "-"]:
                single_write_combination.add(f"{r}w{x}")

    return single_write_combination


def generate_full_write_combination() -> Set[PermissionType]:
    single_write_combination = generate_single_write_combination()
    full_write_combination: Set[PermissionType] = set()

    for owner in single_write_combination:
        for group in single_write_combination:
            for others in single_write_combination:
                permission = PermissionType(permission=f"{owner}{group}{others}")
                full_write_combination.add(permission)

    return full_write_combination


def get_file_permissions(file_path: Union[Path, str]) -> PermissionType:
    return PermissionType(permission=stat.filemode(os.stat(file_path).st_mode)[1:])
