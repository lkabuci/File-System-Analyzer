import os
import tempfile
from pathlib import Path

import pytest

from analyzer.file_statistics_collector import FileStatisticsCollector


def create_temp_file(size_bytes):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"0" * size_bytes)
    return Path(temp_file.name)


@pytest.fixture
def create_temp_files(request):
    temp_files = []

    def _create_temp_files(num_files, file_size):
        for _ in range(num_files):
            temp_file = create_temp_file(file_size)
            temp_files.append(temp_file)
        return temp_files

    yield _create_temp_files

    # Cleanup: Delete temporary files after each test
    for temp_file in temp_files:
        os.unlink(temp_file)


def test_add_file_increments_total_files_and_total_size():
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(b"Test data")
        temp_name = temp.name

    collector = FileStatisticsCollector()

    collector.add_file(Path(temp_name))

    assert collector.total_files == 1
    assert collector.total_size > 0


def test_add_file_updates_average_size():
    collector = FileStatisticsCollector()
    collector.add_file(Path("test_file.txt"))
    collector.add_file(Path("another_test_file.txt"))
    assert collector.average_size == collector.total_size / 2


def test_add_file_updates_smallest_and_largest_file_size(create_temp_files):
    small_file = create_temp_files(1, 100)[0]
    large_file = create_temp_files(1, 1000)[0]

    collector = FileStatisticsCollector()

    collector.add_file(small_file)
    collector.add_file(large_file)

    assert collector.smallest_file_size == os.path.getsize(small_file)
    assert collector.largest_file_size == os.path.getsize(large_file)


def test_add_file_handles_file_not_found():
    collector = FileStatisticsCollector()
    collector.add_file(Path("non_existent_file.txt"))
    assert collector.total_files == 0


def test_report_statistics_outputs_expected_table(create_temp_files):
    temp_files = create_temp_files(1, 100)
    collector = FileStatisticsCollector()

    collector.add_file(temp_files[0])
    collector.report_statistics()


def test_file_statistics_collector(create_temp_files):
    num_files = 10
    file_size = 1024  # 1 KB

    collector = FileStatisticsCollector()

    temp_files = create_temp_files(num_files, file_size)
    for temp_file in temp_files:
        collector.add_file(temp_file)

    collector.report_statistics()

    assert collector.total_files == num_files
    assert collector.total_size == num_files * file_size
    assert collector.average_size == file_size


def test_file_statistics_collector_no_files():
    collector = FileStatisticsCollector()
    collector.report_statistics()
    assert collector.total_files == 0
    assert collector.total_size == 0
    assert collector.average_size == 0
    assert collector.smallest_file_size == float("inf")
    assert collector.largest_file_size == 0
    assert collector.start_time > 0
    assert collector.report_key_len == len("Smallest File Size:   ")


def test_add_file_handles_empty_file(create_temp_files):
    empty_file = create_temp_files(1, 0)[0]

    collector = FileStatisticsCollector()
    collector.add_file(empty_file)

    assert collector.total_files == 1
    assert collector.total_size == 0


def test_add_file_handles_large_file(create_temp_files):
    large_file = create_temp_files(1, 10**6)[0]  # 1 MB

    collector = FileStatisticsCollector()
    collector.add_file(large_file)

    assert collector.total_files == 1
    assert collector.total_size == os.path.getsize(large_file)


def test_report_statistics_calculates_average_size_correctly(create_temp_files):
    small_file = create_temp_files(1, 100)[0]
    large_file = create_temp_files(1, 1000)[0]

    collector = FileStatisticsCollector()
    collector.add_file(small_file)
    collector.add_file(large_file)

    collector.report_statistics()

    assert (
        collector.average_size
        == (os.path.getsize(small_file) + os.path.getsize(large_file)) / 2
    )


def test_report_statistics_calculates_smallest_and_largest_size_correctly(
    create_temp_files,
):
    small_file = create_temp_files(1, 100)[0]
    large_file = create_temp_files(1, 1000)[0]

    collector = FileStatisticsCollector()
    collector.add_file(small_file)
    collector.add_file(large_file)

    collector.report_statistics()

    assert collector.smallest_file_size == os.path.getsize(small_file)
    assert collector.largest_file_size == os.path.getsize(large_file)


def test_report_statistics_calculates_total_size_correctly(create_temp_files):
    small_file = create_temp_files(1, 100)[0]
    large_file = create_temp_files(1, 1000)[0]

    collector = FileStatisticsCollector()
    collector.add_file(small_file)
    collector.add_file(large_file)

    collector.report_statistics()

    assert collector.total_size == os.path.getsize(small_file) + os.path.getsize(
        large_file
    )
