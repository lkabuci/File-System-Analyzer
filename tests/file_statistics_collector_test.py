import os
import tempfile
from pathlib import Path

from analyzer.file_statistics_collector import FileStatisticsCollector


def test_add_file_increments_total_files_and_total_size():
    # Create a temporary file and write some data to it
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(b"Test data")
        temp_name = temp.name

    # Create a FileStatisticsCollector instance
    collector = FileStatisticsCollector()

    # Add the temporary file to the collector
    collector.add_file(Path(temp_name))

    # Assert that the total_files and total_size have been incremented
    assert collector.total_files == 1
    assert collector.total_size > 0

    # Delete the temporary file
    Path(temp_name).unlink()


def test_add_file_updates_average_size():
    collector = FileStatisticsCollector()
    collector.add_file(Path("test_file.txt"))
    collector.add_file(Path("another_test_file.txt"))
    assert collector.average_size == collector.total_size / 2


def test_add_file_updates_smallest_and_largest_file_size():
    # Create a small temporary file and write some data to it
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(b"Test data")
        small_file_name = temp.name

    # Create a large temporary file and write more data to it
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(b"Test data" * 100)
        large_file_name = temp.name

    # Create a FileStatisticsCollector instance
    collector = FileStatisticsCollector()

    # Add the temporary files to the collector
    collector.add_file(Path(small_file_name))
    collector.add_file(Path(large_file_name))

    # Assert that the smallest_file_size and largest_file_size have been updated correctly
    assert collector.smallest_file_size == os.path.getsize(small_file_name)
    assert collector.largest_file_size == os.path.getsize(large_file_name)

    # Delete the temporary files
    Path(small_file_name).unlink()
    Path(large_file_name).unlink()


def test_add_file_handles_file_not_found():
    collector = FileStatisticsCollector()
    collector.add_file(Path("non_existent_file.txt"))
    assert collector.total_files == 0


def test_report_statistics_outputs_expected_table():
    collector = FileStatisticsCollector()
    collector.add_file(Path("test_file.txt"))
    collector.report_statistics()
