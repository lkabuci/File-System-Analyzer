import os
from pathlib import Path

import pyfakefs
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pyfakefs.fake_filesystem_unittest import Patcher
from rich import print

from analyzer.directory_traversal import walk_through_dir
from tests import conftest
from tests.conftest import app_file_system, fake_filesystem_files


def test_normal_walk_through_dir(fs, app_file_system):  # noqa F811
    output = list(walk_through_dir("/root_dir"))
    assert len(output) == len(fake_filesystem_files)
    for item in fake_filesystem_files:
        assert Path(item["name"]) in output  # check if all items are in the output
        assert output.count(Path(item["name"])) == 1  # check for duplicates


def test_walk_through_dir_with_empty_directory(
    fs: FakeFilesystem, app_file_system  # noqa F811
):
    # Create an empty subdirectory
    fs.create_dir("/root_dir/empty_subdir")
    output = list(walk_through_dir("/root_dir/empty_subdir"))
    assert len(output) == 0
    assert output == []


def test_walk_through_dir_with_mixed_permissions(
    fs: FakeFilesystem, app_file_system  # noqa F811
):
    # Change permissions of a file in the fake file system
    fs.chmod("/root_dir/file_100_byte_0644.txt", 0o000)
    fs.chmod("/root_dir/file_100_kb_0444.go", 0o222)
    output = list(walk_through_dir("/root_dir"))
    assert len(output) == len(fake_filesystem_files)

    # check if the file is not excluded due to permission
    assert Path("/root_dir/file_100_byte_0644.txt") in output
    assert Path("/root_dir/file_100_kb_0444.go") in output


def test_walk_through_dir_with_symlink(
    fs: FakeFilesystem, app_file_system  # noqa F811
):
    # Create a symbolic link to a file in the fake file system
    fs.create_symlink("/root_dir/link_to_file.txt", "/root_dir/file_100_byte_0644.txt")

    output = list(walk_through_dir("/root_dir"))
    assert Path("/root_dir/link_to_file.txt") in output
    assert len(output) == len(fake_filesystem_files) + 1
    assert Path("/root_dir/file_100_byte_0644.txt") in output


def test_walk_through_dir_with_permission_error(
    fs: FakeFilesystem, app_file_system, capsys: pytest.CaptureFixture  # noqa F811
):
    # Set permission to None for a directory, causing a PermissionError
    capsys.readouterr()
    dir_with_bad_permission = "/root_dir/bad_permission_dir"
    bad_permission_file = dir_with_bad_permission + "/file_with_bad_permission.txt"
    fs.create_dir(directory_path=dir_with_bad_permission, perm_bits=0o755)
    fs.create_file(bad_permission_file, st_mode=0o222)
    fs.chmod(dir_with_bad_permission, 0o000)  # Set permission to None
    list(walk_through_dir(dir_with_bad_permission))
    assert "Permission error accessing directory" in capsys.readouterr().err
