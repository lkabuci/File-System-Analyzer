from pathlib import Path
from typing import Optional

from rich.prompt import Confirm

from analyzer.Categorization import Categorization
from analyzer.directory_traversal import walk_through_dir
from analyzer.LargeFiles import LargeFileIdentifier
from analyzer.Permission import FilePermissionsChecker
from analyzer.Summary import FileStatisticsCollector
from analyzer.utils.logger import setup_logging
from analyzer.utils.parser import parse_args


def process_directory(
    dir_path: Path,
    size_threshold: Optional[str],
    delete_files: bool,
    log_file: Optional[str],
) -> None:
    """
    Process the target directory.

    Args:
        dir_path (Path): Path to the target directory.
        size_threshold (Optional[str]): Size threshold for large files.
        delete_files (bool): Whether to delete reported files.
        log_file (Optional[str]): Path to the log file.
    """
    file_categorization = Categorization()
    permissions_checker = FilePermissionsChecker()
    large_file_identifier = LargeFileIdentifier(size_threshold)
    file_statistics_collector = FileStatisticsCollector()

    for file_path in walk_through_dir(dir_path):
        file_categorization.add(file_path)
        permissions_checker.add(file_path)
        large_file_identifier.add(file_path)
        file_statistics_collector.add_file(file_path)

    file_categorization.report()
    permissions_checker.report()

    if delete_files and not permissions_checker.is_report_empty() and not log_file:
        confirm = Confirm.ask("Do you want to delete the files with bad permissions?")
        if confirm:
            permissions_checker.delete_reported_files()

    large_file_identifier.report()

    if delete_files and large_file_identifier.large_files and not log_file:
        confirm = Confirm.ask("Do you want to delete the large files?")
        if confirm:
            large_file_identifier.delete_reported_files()

    file_statistics_collector.report_statistics()


def main():
    arguments = parse_args()
    if arguments.target_dir is None:
        exit(1)

    setup_logging(
        log_file=arguments.log_file,
        target_dir=arguments.target_dir,
        size_threshold=arguments.size_threshold,
        delete_files=arguments.delete_files,
    )

    process_directory(
        dir_path=arguments.target_dir,
        size_threshold=str(arguments.size_threshold),
        delete_files=arguments.delete_files,
        log_file=arguments.log_file,
    )


if __name__ == "__main__":
    main()
