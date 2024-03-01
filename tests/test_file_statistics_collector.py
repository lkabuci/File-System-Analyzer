import math
import os
from pathlib import Path

import bitmath
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from analyzer.file_statistics_collector import FileStatisticsCollector
from tests.conftest import app_file_system, create_fakefs_file, fake_filesystem_files


def get_total_size():
    root_dir = Path("/root_dir")
    return sum(file.stat().st_size for file in root_dir.rglob("*") if file.is_file())


@pytest.fixture(scope="function")
def collector(fs, app_file_system):  # noqa F811
    file_statistics_collector = FileStatisticsCollector()
    for file in fake_filesystem_files:
        file_statistics_collector.add_file(Path(file["name"]))
    yield file_statistics_collector


def test_add_file_increments_total_files_and_total_size(fs: FakeFilesystem, collector):
    previous_total_files = collector.total_files
    assert collector.total_files == len(fake_filesystem_files)
    assert collector.total_size > 0

    file_1 = "/root_dir/test_file"
    create_fakefs_file(fs=fs, filepath=file_1)
    collector.add_file(Path(file_1))
    assert collector.total_files == previous_total_files + 1

    file_2 = "/root_dir/test_file_2"
    create_fakefs_file(fs=fs, filepath=file_2)
    collector.add_file(Path(file_2))
    assert collector.total_files == previous_total_files + 2


def test_total_files_size(fs: FakeFilesystem, collector):
    excepted = get_total_size()
    output = collector.total_size
    assert output == excepted

    # Add a new file with 95 bytes
    create_fakefs_file(fs=fs, filepath="/root_dir/test_file", size=bitmath.Byte(95))
    collector.add_file(Path("/root_dir/test_file"))
    assert collector.total_size == excepted + 95


def test_average_size(fs: FakeFilesystem, collector, capsys: pytest.CaptureFixture):
    capsys.readouterr()
    excepted_1 = bitmath.Byte(
        get_total_size() / len(fake_filesystem_files)
    ).best_prefix(bitmath.SI)
    collector.report_statistics()  # cause we only calculating the average once in the report phase (performence reason)

    assert str(excepted_1) in capsys.readouterr().out

    # add large file to upper the average
    create_fakefs_file(
        fs=fs, filepath="/root_dir/test_file", size=bitmath.MiB(400).to_Byte()
    )
    collector.add_file(Path("/root_dir/test_file"))
    collector.report_statistics()

    excepted_2 = bitmath.Byte(
        get_total_size() / (len(fake_filesystem_files) + 1)
    ).best_prefix(bitmath.SI)
    assert str(excepted_2) in capsys.readouterr().out


def test_smallest_file_size(fs: FakeFilesystem, collector):

    smallest_file = "/root_dir/smallest_file"

    excepted = min(file["size"] for file in fake_filesystem_files)
    output = collector.smallest_file_size
    assert output == excepted

    # Add a new file with 1 bytes
    create_fakefs_file(fs=fs, filepath=smallest_file, size=bitmath.Byte(1))
    collector.add_file(Path(smallest_file))
    assert collector.smallest_file_size == Path(smallest_file).stat().st_size


def test_largest_file_size(fs: FakeFilesystem, collector):

    largest_file = "/root_dir/largest_file"

    excepted = max(file["size"] for file in fake_filesystem_files)
    output = collector.largest_file_size
    assert output == excepted

    # Add a new file with 1 GiB
    create_fakefs_file(fs=fs, filepath=largest_file, size=bitmath.GiB(1).to_Byte())
    collector.add_file(Path(largest_file))
    assert collector.largest_file_size == Path(largest_file).stat().st_size


# Now test them all combined
def test_report_statistics(
    fs: FakeFilesystem, collector, capsys: pytest.CaptureFixture
):
    capsys.readouterr()
    collector.report_statistics()
    output = capsys.readouterr().out

    total_files = len(fake_filesystem_files)
    _total_size_in_bytes = get_total_size()
    total_size = bitmath.Byte(_total_size_in_bytes).best_prefix(bitmath.SI)
    average_size = bitmath.Byte(_total_size_in_bytes / total_files).best_prefix(
        bitmath.SI
    )
    smallest_file = bitmath.Byte(
        int(min(file["size"] for file in fake_filesystem_files))
    ).best_prefix(bitmath.SI)
    largest_file = bitmath.Byte(
        int(max(file["size"] for file in fake_filesystem_files))
    ).best_prefix(bitmath.SI)

    assert "Total Files:" in output
    assert "Total Size:" in output
    assert "Average File Size:" in output
    assert "Smallest File Size:" in output
    assert "Largest File Size:" in output
    assert "Time Elapsed:" in output

    assert str(total_files) in output
    assert str(total_size) in output
    assert str(average_size) in output
    assert str(smallest_file) in output
    assert str(largest_file) in output
