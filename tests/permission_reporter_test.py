import tempfile
from pathlib import Path

import pytest

from analyzer.permission_reporter import FilePermissionsChecker, convert_octal_to_rwx


def test_convert_octal_to_rwx():
    assert convert_octal_to_rwx("777") == "rwxrwxrwx"
    assert convert_octal_to_rwx("666") == "rw-rw-rw-"
    assert convert_octal_to_rwx("400") == "r--------"
    assert convert_octal_to_rwx("644") == "rw-r--r--"
    assert convert_octal_to_rwx("000") == "---------"


def test_convert_octal_to_rwx_with_invalid_input():
    with pytest.raises(ValueError):
        convert_octal_to_rwx("888")


def test_convert_octal_to_rwx_with_non_string_input():
    with pytest.raises(TypeError):
        convert_octal_to_rwx(777)


def test_convert_octal_to_rwx_with_empty_string():
    with pytest.raises(ValueError):
        convert_octal_to_rwx("")


def test_convert_octal_to_rwx_with_partial_octal():
    assert convert_octal_to_rwx("7") == "rwx"
    assert convert_octal_to_rwx("6") == "rw-"
    assert convert_octal_to_rwx("4") == "r--"
    assert convert_octal_to_rwx("0") == "---"


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
