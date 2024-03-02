import logging
import sys

from rich.prompt import Confirm

from analyzer.directory_traversal import walk_through_dir
from analyzer.file_categorization import FileCategorization
from analyzer.file_statistics_collector import FileStatisticsCollector
from analyzer.large_files_identification import LargeFileIdentifier
from analyzer.permission_reporter import FilePermissionsChecker
from analyzer.utils.logger import LogInfo, configure_log_file, log_intro
from analyzer.utils.parser import parse_args


def process_directory(dir_path, size_threshold: str, delete_files, log_file) -> None:
    """
    Process the target directory.

    Args:
        dir_path (Path): Path to the target directory.
        size_threshold (Optional[int]): Size threshold for large files.
        delete_files (bool): Whether to delete reported files.
        log_file (Optional[str]): Path to the log file.
    """
    file_categorization = FileCategorization()
    permissions_checker = FilePermissionsChecker()
    large_file_identifier = LargeFileIdentifier(size_threshold)
    file_statistics_collector = FileStatisticsCollector()

    for file_path in walk_through_dir(dir_path):
        file_categorization.add_file(file_path)
        permissions_checker.check_permissions(file_path)
        large_file_identifier.add_file(file_path)
        file_statistics_collector.add_file(file_path)

    file_categorization.display_summary()
    permissions_checker.print_permission_report()

    if delete_files and not permissions_checker.is_report_empty() and not log_file:
        confirm = Confirm.ask("Do you want to delete the files with bad permissions?")
        if confirm:
            permissions_checker.delete_reported_files()

    large_file_identifier.report_large_files()

    if delete_files and large_file_identifier.large_files and not log_file:
        confirm = Confirm.ask("Do you want to delete the large files?")
        if confirm:
            large_file_identifier.delete_reported_files()

    file_statistics_collector.report_statistics()


def main():
    arguments = parse_args()
    if arguments.target_dir is None:
        exit(1)

    logging.basicConfig(
        filename=arguments.log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    configure_log_file(arguments.log_file)
    log_intro(
        LogInfo(
            target_dir=arguments.target_dir,
            size_threshold=arguments.size_threshold,
            delete_files=arguments.delete_files,
            log_file=arguments.log_file,
        )
    )

    process_directory(
        dir_path=arguments.target_dir,
        size_threshold=str(arguments.size_threshold),
        delete_files=arguments.delete_files,
        log_file=arguments.log_file,
    )


if __name__ == "__main__":
    main()
