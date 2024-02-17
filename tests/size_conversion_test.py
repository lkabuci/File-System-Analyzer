from pathlib import Path

import pytest

from analyzer.large_files_identification import LargeFileIdentifier, convert_size


def test_convert_size_to_kb():
    assert convert_size(1024, "KB") == "1.00 KB"


def test_convert_size_to_mb():
    assert convert_size(1024 * 1024, "MB") == "1.00 MB"


def test_large_file_identifier_add_file():
    identifier = LargeFileIdentifier(size_threshold=1024)
    identifier.add_file(Path(__file__))
    assert len(identifier.large_files) > 0


def test_large_file_identifier_add_file_below_threshold():
    identifier = LargeFileIdentifier(size_threshold=1024 * 1024 * 1024)  # 1GB
    identifier.add_file(Path(__file__))
    assert len(identifier.large_files) == 0


def test_large_file_identifier_scan_and_report(capsys):
    identifier = LargeFileIdentifier(size_threshold=1024)
    identifier.add_file(Path(__file__))
    identifier.scan_and_report("KB")
    captured = capsys.readouterr()
    assert "Large Files" in captured.out


def test_large_file_identifier_delete_non_existent_files():
    identifier = LargeFileIdentifier(size_threshold=1024)
    temp_file = Path("non_existent_file.txt")

    # Try to delete a non-existent file
    identifier.add_file(temp_file)
    identifier.delete_reported_files()

    # Check that the file still does not exist
    assert not temp_file.exists()


def test_large_file_identifier_scan_and_report_no_large_files(capsys):
    identifier = LargeFileIdentifier(size_threshold=1024)

    # Scan and report when no large files are added
    identifier.scan_and_report("KB")
    captured = capsys.readouterr()

    assert "No large files found" in captured.out


def test_large_file_identifier_custom_size_threshold():
    custom_threshold = 500  # Set a custom size threshold
    identifier = LargeFileIdentifier(size_threshold=custom_threshold)

    # Add a file larger than the custom threshold
    large_file = Path("large_file.txt")
    large_file.write_text("A" * (custom_threshold + 1))
    identifier.add_file(large_file)

    assert len(identifier.large_files) == 1
    assert identifier.large_files[0].file_path == large_file
