import pytest

from analyzer.file_categorization import FileCategorization


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
