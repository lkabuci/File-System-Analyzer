from pathlib import Path

import bitmath
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from analyzer.Categorization import Categorization
from tests.conftest import app_file_system, create_fakefs_file, fake_filesystem_files


@pytest.fixture(scope="function")
def categorization(fs: FakeFilesystem, app_file_system):  # noqa F811
    categorization_instance = Categorization()
    for file in fake_filesystem_files:
        categorization_instance.add(str(file["name"]))
    yield categorization_instance


def test_empty_categorization(capsys: pytest.CaptureFixture):
    capsys.readouterr()
    categorization_instance = Categorization()
    assert len(categorization_instance.category_data) == 0
    categorization_instance.report()
    assert "No files to categorize." in capsys.readouterr().out


def test_single_file(fs: FakeFilesystem, capsys: pytest.CaptureFixture):
    capsys.readouterr()

    # Check first that it's empty
    categorization_instance = Categorization()
    assert len(categorization_instance.category_data) == 0

    filename = Path("/script.py")
    create_fakefs_file(fs, filename, 0o644, bitmath.Byte(100))
    categorization_instance.add(filename)

    assert len(categorization_instance.category_data) == 1


def test_add_file(fs: FakeFilesystem):
    fs.create_file("/test.txt", contents="This is a test file")
    fs.create_file("/test.mp4", contents="This is a test video file")
    categorization_instance = Categorization()

    categorization_instance.add(Path("/test.txt"))
    categorization_instance.add(Path("/test.mp4"))

    assert len(categorization_instance.category_data) == 2
    assert categorization_instance.category_data["Text"].number_of_files == 1
    assert categorization_instance.category_data["Video"].number_of_files == 1


def test_display_summary(fs: FakeFilesystem, capsys: pytest.CaptureFixture):
    fs.create_file("/test.txt", contents="This is a test file")
    fs.create_file("/test.mp4", contents="This is a test video file")
    categorization_instance = Categorization()
    categorization_instance.add(Path("/test.txt"))
    categorization_instance.add(Path("/test.mp4"))

    categorization_instance.report()

    captured = capsys.readouterr()
    assert "Text" in captured.out
    assert "Video" in captured.out
    assert "1" in captured.out  # number of files in each category


def test_add_file_multiple_files_same_category(fs: FakeFilesystem):
    fs.create_file("/test1.txt", contents="This is a test file")
    fs.create_file("/test2.txt", contents="This is another test file")
    categorization_instance = Categorization()

    categorization_instance.add(Path("/test1.txt"))
    categorization_instance.add(Path("/test2.txt"))

    assert len(categorization_instance.category_data) == 1
    assert categorization_instance.category_data["Text"].number_of_files == 2


def test_add_file_different_sizes(fs: FakeFilesystem):
    fs.create_file("/small.txt", contents="small file")
    fs.create_file("/large.txt", contents="large file" * 1000)
    categorization_instance = Categorization()

    categorization_instance.add(Path("/small.txt"))
    categorization_instance.add(Path("/large.txt"))

    assert len(categorization_instance.category_data) == 1
    assert categorization_instance.category_data["Text"].number_of_files == 2
    assert categorization_instance.category_data["Text"].total_size > bitmath.KiB(1)


def test_display_summary_multiple_files_same_category(
    fs: FakeFilesystem, capsys: pytest.CaptureFixture
):
    fs.create_file("/test1.txt", contents="This is a test file")
    fs.create_file("/test2.txt", contents="This is another test file")
    categorization_instance = Categorization()
    categorization_instance.add(Path("/test1.txt"))
    categorization_instance.add(Path("/test2.txt"))

    categorization_instance.report()

    captured = capsys.readouterr()
    assert "Text" in captured.out
    assert "2" in captured.out  # number of files in the category


def test_large_filesystem(categorization, capsys: pytest.CaptureFixture):
    capsys.readouterr()

    # Check that the number of files in the categorization is the same as the number of files in the filesystem
    assert sum(
        category_info.number_of_files
        for category_info in categorization.category_data.values()
    ) == len(fake_filesystem_files)

    # Check that the total size of the files in the categorization is the same as the total size of the files in the filesystem
    assert sum(
        category_info.total_size
        for category_info in categorization.category_data.values()
    ) == sum(file["size"] for file in fake_filesystem_files)


def test_report_output(categorization, capsys: pytest.CaptureFixture):
    categorization.report()
    captured = capsys.readouterr()

    # headers
    assert "File Summary" in captured.out
    assert "Category" in captured.out
    assert "File Extension" in captured.out
    assert "Number of files" in captured.out
    assert "Size" in captured.out

    # Values
    assert "Text" in captured.out
    assert "Development" in captured.out
    assert "Archive" in captured.out
    assert "Audio" in captured.out
