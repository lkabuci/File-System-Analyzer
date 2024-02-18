import os
from pathlib import Path

import pytest

from analyzer.file_categorization import FileCategorization, convert_size


@pytest.fixture
def test_files(tmp_path):
    # Create test files with different extensions
    file1 = tmp_path / "file1.txt"
    file1.write_text("content 1")

    file2 = tmp_path / "file2.py"
    file2.write_text("content 2")

    file3 = tmp_path / "file3.jpg"
    file3.write_text("content 3")

    file4 = tmp_path / "file4.mp3"
    file4.write_text("content 4")

    return [file1, file2, file3, file4]


def test_add_file_and_display_summary(test_files, capsys):
    categorization = FileCategorization()

    for file in test_files:
        categorization.add_file(file)

    categorization.display_summary()

    captured = capsys.readouterr()
    assert "File Summary" in captured.out
    assert "Category" in captured.out
    assert "File Extension" in captured.out
    assert "Number of Files" in captured.out
    assert "Size" in captured.out


def create_tmp_file(name: str, size: int) -> Path:
    with open(name, "wb") as f:
        f.write(os.urandom(size))
    return Path(name)


def test_add_file_increments_count_and_size():
    file_categorization = FileCategorization()
    tmp_file = create_tmp_file("tmp1.txt", 1024)
    file_categorization.add_file(tmp_file)
    assert file_categorization.grouped_files["Text"][".txt"]["count"] == 1
    assert file_categorization.grouped_files["Text"][".txt"]["size"] == 1024
    os.unlink(tmp_file)


def test_add_file_handles_nonexistent_file():
    file_categorization = FileCategorization()
    file_categorization.add_file(Path("nonexistent.txt"))
    assert file_categorization.grouped_files["Other"][".txt"]["size"] == 0


def test_update_table_creates_table_with_correct_columns():
    file_categorization = FileCategorization()
    tmp_file = create_tmp_file("tmp2.txt", 2048)
    file_categorization.add_file(tmp_file)
    file_categorization.update_table()
    assert len(file_categorization.table.columns) == 4
    assert [column.header for column in file_categorization.table.columns] == [
        "Category",
        "File Extension",
        "Number of Files",
        "Size",
    ]
    os.unlink(tmp_file)


def test_convert_size_returns_correct_unit():
    assert convert_size(1024, "KB") == "1.00 KB"
    assert convert_size(1024, "MB") == "1.00 MB"
    assert convert_size(1024, "GB") == "1.00 GB"


def test_get_category_returns_correct_category():
    file_categorization = FileCategorization()
    assert file_categorization._get_category(".txt") == "Text"
    assert file_categorization._get_category(".nonexistent") == "Other"
