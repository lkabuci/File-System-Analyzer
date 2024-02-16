import tempfile
from pathlib import Path

import pytest

from analyzer.permission_reporter import FilePermissionsChecker


def test_convert_octal_to_rwx():
    checker = FilePermissionsChecker()
    assert checker._convert_octal_to_rwx("777") == "rwxrwxrwx"
    assert checker._convert_octal_to_rwx("666") == "rw-rw-rw-"
    assert checker._convert_octal_to_rwx("400") == "r--------"
    assert checker._convert_octal_to_rwx("644") == "rw-r--r--"
    assert checker._convert_octal_to_rwx("000") == "---------"


def test_convert_octal_to_rwx_with_invalid_input():
    checker = FilePermissionsChecker()
    with pytest.raises(ValueError):
        checker._convert_octal_to_rwx("888")


def test_convert_octal_to_rwx_with_non_string_input():
    checker = FilePermissionsChecker()
    with pytest.raises(TypeError):
        checker._convert_octal_to_rwx(777)


def test_convert_octal_to_rwx_with_empty_string():
    checker = FilePermissionsChecker()
    with pytest.raises(ValueError):
        checker._convert_octal_to_rwx("")


def test_convert_octal_to_rwx_with_partial_octal():
    checker = FilePermissionsChecker()
    assert checker._convert_octal_to_rwx("7") == "rwx"
    assert checker._convert_octal_to_rwx("6") == "rw-"
    assert checker._convert_octal_to_rwx("4") == "r--"
    assert checker._convert_octal_to_rwx("0") == "---"


def test_check_permissions():
    checker = FilePermissionsChecker()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "temp_file"
        temp_file.touch()
        temp_file.chmod(0o777)
        checker.check_permissions(temp_file)
        assert temp_file in checker.reported_files


def test_check_permissions_with_bad_permissions():
    checker = FilePermissionsChecker()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "temp_file"
        temp_file.touch()
        temp_file.chmod(0o666)
        checker.check_permissions(temp_file)
        assert temp_file in checker.reported_files
