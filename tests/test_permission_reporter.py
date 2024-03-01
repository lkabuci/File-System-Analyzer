from collections import Counter
from pathlib import Path
from typing import List, Tuple

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from rich import print
from rich.table import Table

from analyzer.permission_reporter import FilePermissionsChecker
from tests.conftest import app_file_system, create_fakefs_file, fake_filesystem_files


def extract_file_permissions_from_table(table: Table) -> List[Tuple[str, str]]:
    files: List[str] = table.columns[0]._cells
    perms: List[str] = table.columns[1]._cells
    return list(zip(files, perms))


@pytest.fixture(scope="function")
def permission_instance(fs, app_file_system: FakeFilesystem):  # noqa F811
    perm = FilePermissionsChecker()
    for file in fake_filesystem_files:
        perm.check_permissions(Path(file["name"]))
    yield perm


def test_normal_permission_reporter(
    fs: FakeFilesystem, permission_instance: FilePermissionsChecker
):
    file_permissions = extract_file_permissions_from_table(permission_instance._table)
    assert (
        len(file_permissions) == 9
    )  # 9 is the number of files that have bad permissions inside fake_filesystem_files


def test_empty_permission_reporter(capsys: pytest.CaptureFixture):
    perm = FilePermissionsChecker()
    capsys.readouterr()
    files_perms = extract_file_permissions_from_table(perm._table)
    perm.print_permission_report()
    assert perm.is_report_empty()
    assert len(perm._table.rows) == len(files_perms) == 0
    assert "No files with bad permissions found." in capsys.readouterr().out


def test_single_permission(fs: FakeFilesystem):
    perm = FilePermissionsChecker()
    file_path = create_fakefs_file(
        fs=fs, filepath="/root_dir/parent5/file_300_byte_0600.html", mode=0o222
    )
    perm.check_permissions(file_path)
    assert not perm.is_report_empty()
    assert len(perm._table.rows) == 1
    assert perm._table.columns[0]._cells[0] == str(file_path)
    assert perm._table.columns[1]._cells[0] == "-w--w--w-"


def test_check_good_permission_file(fs: FakeFilesystem):
    perm = FilePermissionsChecker()
    file_path = create_fakefs_file(
        fs=fs, filepath="/root_dir/parent5/file_300_byte_0600.html", mode=0o644
    )
    perm.check_permissions(file_path)
    assert perm.is_report_empty()
    assert len(perm._table.rows) == 0


def test_multiple_files_with_bad_permissions(fs: FakeFilesystem):
    perm = FilePermissionsChecker()
    list_of_files_with_bad_permission = [
        ["/file_000_permission", 0o000],
        ["/file_777_permission", 0o777],
        ["/file_555_permission", 0o555],
        ["/file_752_permission", 0o373],
    ]

    for filename, mode in list_of_files_with_bad_permission:
        file_path = create_fakefs_file(fs=fs, filepath=filename, mode=mode)
        perm.check_permissions(file_path)

    assert not perm.is_report_empty()
    assert len(perm._table.rows) == len(list_of_files_with_bad_permission)

    extracted_files = [
        file for file, _ in extract_file_permissions_from_table(perm._table)
    ]
    expected_files = [file for file, _ in list_of_files_with_bad_permission]
    assert Counter(extracted_files) == Counter(expected_files)


def test_delete_reported_files(permission_instance: FilePermissionsChecker):
    assert not permission_instance.is_report_empty()
    assert all(
        Path(file).exists()
        for file, _ in extract_file_permissions_from_table(permission_instance._table)
    )

    permission_instance.delete_reported_files()
    assert all(
        not Path(file).exists()
        for file, _ in extract_file_permissions_from_table(permission_instance._table)
    )


def test_report(permission_instance, capsys: pytest.CaptureFixture):
    permission_instance.print_permission_report()
    std = capsys.readouterr()

    assert not permission_instance.is_report_empty()
    assert "No files with bad permissions found." not in std.out

    # Test headers
    assert "Permission Report" in std.out
    assert "File" in std.out
    assert "Permissions" in std.out