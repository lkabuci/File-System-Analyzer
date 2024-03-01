import math
import os
from collections import Counter
from pathlib import Path

import bitmath
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from analyzer.large_files_identification import LargeFileIdentifier
from tests.conftest import app_file_system, create_fakefs_file, fake_filesystem_files


def get_large_files_in_fake_files(
    size: bitmath.Byte = LargeFileIdentifier.DEFAULT_THRESHOLD.to_Byte(),
):
    return [file for file in fake_filesystem_files if file["size"] >= size]


@pytest.fixture(scope="function")
def LargeFileIdentifier_(fs: FakeFilesystem, app_file_system):  # noqa F811
    instance = LargeFileIdentifier(size_threshold="1024 KiB")
    for file in fake_filesystem_files:
        instance.add_file(Path(file["name"]))
    yield instance


def test_empty_large_files():
    large_files = LargeFileIdentifier()
    assert len(large_files.large_files) == 0


def test_add_large_file(fs: FakeFilesystem):
    large_files = LargeFileIdentifier()

    large_file_path = "/large_file.txt"
    large_size = int(large_files.DEFAULT_THRESHOLD.to_Byte().value) + 1

    assert len(large_files.large_files) == 0

    fs.create_file(
        file_path=large_file_path,
        st_size=large_size,
        create_missing_dirs=True,
    )
    large_files.add_file(large_file_path)
    assert len(large_files.large_files) == 1
    assert large_files.large_files[0].file_path == large_file_path
    assert large_files.large_files[0].size == bitmath.Byte(large_size)


def test_add_small_file(fs: FakeFilesystem):
    large_files = LargeFileIdentifier()

    small_file_path = "/small_file.txt"
    small_size = int(large_files.DEFAULT_THRESHOLD.to_Byte().value) - 1

    assert len(large_files.large_files) == 0

    fs.create_file(
        file_path=small_file_path,
        st_size=small_size,
        create_missing_dirs=True,
    )
    large_files.add_file(small_file_path)
    assert len(large_files.large_files) == 0


def test_default_threshold(fs: FakeFilesystem):
    large_files = LargeFileIdentifier()

    file = "/file.txt"
    fs.create_file(file, st_size=int(large_files.DEFAULT_THRESHOLD.to_Byte().value))
    large_files.add_file(file)
    assert len(large_files.large_files) == 1
    assert large_files.size_threshold == large_files.DEFAULT_THRESHOLD
    assert large_files.large_files[0].size == large_files.DEFAULT_THRESHOLD


def test_add_file_with_threshold(fs: FakeFilesystem):
    large_files = LargeFileIdentifier(size_threshold="1 KiB")

    small_file_path = "/small_file.txt"
    small_size = int(large_files.size_threshold.to_Byte().value) - 10

    assert len(large_files.large_files) == 0

    fs.create_file(
        file_path=small_file_path,
        st_size=small_size,
        create_missing_dirs=True,
    )
    large_files.add_file(small_file_path)
    assert len(large_files.large_files) == 0


def test_add_file_with_invalid_threshold():
    with pytest.raises(ValueError):
        LargeFileIdentifier(size_threshold="1 KiBb")


def test_add_file_larger_than_threshold(fs: FakeFilesystem):
    large_files = LargeFileIdentifier(size_threshold="1 KiB")

    large_file_path = "/large_file.txt"
    large_size = int(large_files.size_threshold.to_Byte().value) + 10

    assert len(large_files.large_files) == 0

    fs.create_file(
        file_path=large_file_path,
        st_size=large_size,
        create_missing_dirs=True,
    )
    large_files.add_file(large_file_path)
    assert len(large_files.large_files) == 1
    assert large_files.large_files[0].file_path == large_file_path
    assert large_files.large_files[0].size == bitmath.Byte(large_size)


def test_normal_case(fs: FakeFilesystem, LargeFileIdentifier_):
    excepted = [
        file["name"]
        for file in fake_filesystem_files
        if file["size"] >= LargeFileIdentifier_.size_threshold
    ]
    output = [str(file.file_path) for file in LargeFileIdentifier_.large_files]

    assert Counter(excepted) == Counter(output)


def test_check_reported_files_sorted(LargeFileIdentifier_):
    assert all(
        LargeFileIdentifier_.large_files[i].size
        <= LargeFileIdentifier_.large_files[i + 1].size
        for i in range(len(LargeFileIdentifier_.large_files) - 1)
    )


def test_check_sorted_files_are_updating(fs: FakeFilesystem):
    large_files_sorted = LargeFileIdentifier(size_threshold="1 KiB")

    list_of_large_files = [
        {"name": "/file3.txt", "size": bitmath.KiB(3).to_Byte()},
        {"name": "/file1.txt", "size": bitmath.KiB(1).to_Byte()},
        {"name": "/file2.txt", "size": bitmath.KiB(2).to_Byte()},
    ]

    for file in list_of_large_files:
        fs.create_file(
            file_path=file["name"],
            st_size=int(file["size"].value),
        )
        large_files_sorted.add_file(file["name"])

    assert len(large_files_sorted.large_files) == len(list_of_large_files)
    assert all(
        large_files_sorted.large_files[i].size
        <= large_files_sorted.large_files[i + 1].size
        for i in range(len(large_files_sorted.large_files) - 1)
    )

    # Add another large file to check if they are updating
    another_large_file = "/file4.txt"
    fs.create_file(another_large_file, st_size=int(bitmath.KiB(2).to_Byte().value))
    large_files_sorted.add_file(another_large_file)

    assert len(large_files_sorted.large_files) == len(list_of_large_files) + 1
    assert all(
        large_files_sorted.large_files[i].size
        <= large_files_sorted.large_files[i + 1].size
        for i in range(len(large_files_sorted.large_files) - 1)
    )


def test_report(LargeFileIdentifier_, capsys: pytest.CaptureFixture):

    capsys.readouterr()

    list_of_large_files = [
        file
        for file in fake_filesystem_files
        if file["size"] >= LargeFileIdentifier_.size_threshold
    ]

    LargeFileIdentifier_.report_large_files()

    output = capsys.readouterr().out

    # headers
    assert "Large Files" in output
    assert "File Path" in output
    assert "Size" in output

    # content
    for file in list_of_large_files:
        assert file["name"] in output
        assert str(file["size"].best_prefix(bitmath.SI)) in output