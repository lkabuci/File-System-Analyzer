from pathlib import Path
from typing import Optional

from rich.prompt import Confirm

from analyzer.Categorization import Categorization
from analyzer.directory_traversal import walk_through_dir
from analyzer.LargeFiles import LargeFileIdentifier
from analyzer.Permission import FilePermissionsChecker
from analyzer.Summary import FileStatisticsCollector


def process_files(
    dir_path: Path,
    file_categorization: Categorization,
    permissions_checker: FilePermissionsChecker,
    large_file_identifier: LargeFileIdentifier,
    file_statistics_collector: FileStatisticsCollector,
) -> None:
    for file_path in walk_through_dir(dir_path):
        file_categorization.add(file_path)
        permissions_checker.add(file_path)
        large_file_identifier.add(file_path)
        file_statistics_collector.add_file(file_path)


def handle_permissions(
    delete_files: bool,
    permissions_checker: FilePermissionsChecker,
    log_file: Optional[str],
) -> None:
    if delete_files and not permissions_checker.is_report_empty() and not log_file:
        confirm = Confirm.ask("Do you want to delete the files with bad permissions?")
        if confirm:
            permissions_checker.delete_reported_files()


def handle_large_files(
    delete_files: bool,
    large_file_identifier: LargeFileIdentifier,
    log_file: Optional[str],
) -> None:
    if delete_files and large_file_identifier.large_files and not log_file:
        confirm = Confirm.ask("Do you want to delete the large files?")
        if confirm:
            large_file_identifier.delete_reported_files()


def process_directory(
    dir_path: Path,
    size_threshold: Optional[str],
    delete_files: bool,
    log_file: Optional[str],
) -> None:
    file_categorization = Categorization()
    permissions_checker = FilePermissionsChecker()
    large_file_identifier = LargeFileIdentifier(size_threshold)
    file_statistics_collector = FileStatisticsCollector()

    process_files(
        dir_path,
        file_categorization,
        permissions_checker,
        large_file_identifier,
        file_statistics_collector,
    )

    file_categorization.report()
    permissions_checker.report()
    handle_permissions(delete_files, permissions_checker, log_file)
    large_file_identifier.report()
    handle_large_files(delete_files, large_file_identifier, log_file)
    file_statistics_collector.report_statistics()
