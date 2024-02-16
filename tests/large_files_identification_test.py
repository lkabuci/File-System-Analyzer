import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from analyzer.large_files_identification import LargeFileIdentifier


@pytest.fixture
def test_large_file_identifier():
    return LargeFileIdentifier(size_threshold=1024)


def create_temp_file(size_bytes):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"0" * size_bytes)
    return Path(temp_file.name)


def test_large_file_identifier_add_file(test_large_file_identifier, tmp_path):
    # Create small and large temp files
    small_file = create_temp_file(size_bytes=512)
    large_file = create_temp_file(size_bytes=2048)

    # Add files to LargeFileIdentifier
    test_large_file_identifier.add_file(small_file)
    test_large_file_identifier.add_file(large_file)

    # Check that the large file is added, and the small file is not
    assert len(test_large_file_identifier.large_files) == 1
    assert test_large_file_identifier.large_files[0].file_path == large_file


def test_large_file_identifier_scan_and_report(
    test_large_file_identifier, capsys, tmp_path
):
    # Create small and large temp files
    small_file = create_temp_file(size_bytes=512)
    large_file = create_temp_file(size_bytes=2048)

    # Add files to LargeFileIdentifier
    test_large_file_identifier.add_file(small_file)
    test_large_file_identifier.add_file(large_file)

    # Mock user input to simulate user pressing 'n' when prompted
    with patch("builtins.input", return_value="n"):
        # Scan and report
        test_large_file_identifier.scan_and_report()

    # Check the printed output
    captured = capsys.readouterr()
    assert "Large Files" in captured.out

    # Check if the large file entry is present in the output
    assert str(large_file) in captured.out
    assert str(2048) in captured.out

    # Check if the small file entry is not present in the output
    assert str(small_file) not in captured.out
    assert str(512) not in captured.out


def test_large_file_identifier_delete_reported_files(
    test_large_file_identifier, capsys, tmp_path
):
    # Create small and large temp files
    small_file = create_temp_file(size_bytes=512)
    large_file = create_temp_file(size_bytes=2048)

    # Add files to LargeFileIdentifier
    test_large_file_identifier.add_file(small_file)
    test_large_file_identifier.add_file(large_file)

    # Delete reported files
    test_large_file_identifier.delete_reported_files()

    # Check the printed output
    captured = capsys.readouterr()
    assert "Deleted" in captured.out
    assert large_file.exists() is False
    assert small_file.exists() is True  # Small file should not be deleted
