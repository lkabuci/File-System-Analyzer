from pathlib import Path

import pytest

from analyzer.large_files_identification import LargeFileIdentifier

DEFAULT_THRESHOLD_STR = "1MiB"
CUSTOM_THRESHOLD_STR = "500MiB"
INVALID_THRESHOLD_STR = "invalid_unit"


@pytest.fixture
def identifier():
    return LargeFileIdentifier(size_threshold=DEFAULT_THRESHOLD_STR)


# TODO: fix the test the file is too small to be considered large
# def test_large_file_identifier_add_file(identifier):
#     identifier.add_file(Path(__file__))
#     assert len(identifier.large_files) > 0


def test_large_file_identifier_add_file_below_threshold():
    identifier = LargeFileIdentifier(size_threshold="1GiB")  # 1GB
    identifier.add_file(Path(__file__))
    assert len(identifier.large_files) == 0


def test_large_file_identifier_delete_non_existent_files(identifier):
    temp_file = Path("non_existent_file.txt")

    # Try to delete a non-existent file
    identifier.add_file(temp_file)
    identifier.delete_reported_files()

    # Check that the file still does not exist
    assert not temp_file.exists()


def test_large_file_identifier_scan_and_report_no_large_files(capsys, identifier):
    # Scan and report when no large files are added
    identifier.report_large_files()
    captured = capsys.readouterr()
    assert "No large files found" in captured.out


def test_large_file_identifier_custom_size_threshold():
    identifier = LargeFileIdentifier(size_threshold=CUSTOM_THRESHOLD_STR)

    # Add a file larger than the custom threshold
    large_file = Path("large_file.txt")
    large_file.write_text("A" * (500 * 1024 * 1024 + 1))
    identifier.add_file(large_file)

    assert len(identifier.large_files) == 1
    assert identifier.large_files[0].file_path == large_file
    large_file.unlink()


def test_large_file_identifier_custom_size_threshold_invalid():
    with pytest.raises(ValueError, match="Invalid size threshold format"):
        LargeFileIdentifier(size_threshold=INVALID_THRESHOLD_STR)


def test_large_file_identifier_custom_size_threshold_none():
    identifier = LargeFileIdentifier(size_threshold=None)
    assert identifier.size_threshold == LargeFileIdentifier.DEFAULT_THRESHOLD


def test_large_file_identifier_delete_one_file_at_a_time(capsys, identifier, mocker):
    mocker.patch("analyzer.large_files_identification.Prompt.ask", return_value="y")

    large_file = Path("large_file.txt")
    large_file.write_text(
        "A" * (int(DEFAULT_THRESHOLD_STR.replace("MiB", "")) * 1024 * 1024 + 1)
    )
    identifier.add_file(large_file)

    identifier.delete_one_file_at_a_time()
    captured = capsys.readouterr()

    assert "Deleted" in captured.out
    assert not large_file.exists()


def test_large_file_identifier_delete_one_file_at_a_time_skip(
    capsys, identifier, mocker
):
    mocker.patch("analyzer.large_files_identification.Prompt.ask", return_value="n")

    large_file = Path("large_file.txt")
    large_file.write_text(
        "A" * (int(DEFAULT_THRESHOLD_STR.replace("MiB", "")) * 1024 * 1024 + 1)
    )
    identifier.add_file(large_file)

    identifier.delete_one_file_at_a_time()
    captured = capsys.readouterr()

    assert "Deleted" not in captured.out
    assert large_file.exists()

