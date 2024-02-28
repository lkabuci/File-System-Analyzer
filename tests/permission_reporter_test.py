import tempfile
from pathlib import Path

import pytest

from analyzer.permission_reporter import FilePermissionsChecker


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
