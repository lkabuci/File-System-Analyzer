from test.conftest import create_fakefs_file
from typing import Dict, List, Union

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from analyzer.utils.permissions import (
    PermissionType,
    generate_full_write_combination,
    get_file_permissions,
)


def test_generate_full_write_combination():
    full_write_combination = generate_full_write_combination()

    # Ensure that the return value is a set of PermissionType
    assert isinstance(full_write_combination, set)
    assert all(isinstance(item, PermissionType) for item in full_write_combination)

    # Ensure that all the permissions have at least one "w" in them
    for permission in full_write_combination:
        assert "w" in permission.permission[0:3]
        assert "w" in permission.permission[3:6]
        assert "w" in permission.permission[6:9]


def test_get_file_permissions(fs: FakeFilesystem):
    files: List[Dict[str, Union[int, str]]] = [
        {"path": "/test_1.txt", "mode": 0o644, "expected_permission": "rw-r--r--"},
        {"path": "/test_2.txt", "mode": 0o000, "expected_permission": "---------"},
        {"path": "/test_3.txt", "mode": 0o777, "expected_permission": "rwxrwxrwx"},
        {"path": "/test_4.txt", "mode": 0o222, "expected_permission": "-w--w--w-"},
        {"path": "/test_5.txt", "mode": 0o400, "expected_permission": "r--------"},
        {"path": "/test_6.txt", "mode": 0o600, "expected_permission": "rw-------"},
    ]

    for file in files:
        create_fakefs_file(fs, filepath=str(file["path"]), mode=int(file["mode"]))
        expected_permission = PermissionType(
            permission=str(file["expected_permission"])
        )
        assert get_file_permissions(str(file["path"])) == expected_permission


def test_get_file_permissions_nonexistent_file():
    non_existent_file = "/non_existent.txt"

    with pytest.raises(FileNotFoundError):
        get_file_permissions(non_existent_file)


def test_get_file_permissions_directory(fs: FakeFilesystem):
    fs.create_dir("/test_dir", perm_bits=0o755)
    expected_permission = PermissionType(permission="rwxr-xr-x")

    actual_permission = get_file_permissions("/test_dir")

    assert actual_permission == expected_permission


def test_get_file_permissions_symlink(fs: FakeFilesystem):
    create_fakefs_file(fs, "/test.txt", mode=0o644)
    fs.create_symlink("/link.txt", "/test.txt")
    expected_permission = PermissionType(permission="rw-r--r--")

    actual_permission = get_file_permissions("/link.txt")

    assert actual_permission == expected_permission
