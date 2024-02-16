import logging
import sys
from datetime import datetime
from pathlib import Path

from rich.prompt import Confirm

from analyzer.directory_traversal import walk_through_dir
from analyzer.file_categorization import FileCategorization
from analyzer.large_files_identification import LargeFileIdentifier
from analyzer.permission_reporter import FilePermissionsChecker
from analyzer.utils.parser import parse_args


def configure_log_file(log_file):
    """
    Configure log file redirection if provided.
    """
    if log_file:
        sys.stdout = open(log_file, "a")
        sys.stderr = open(log_file, "a")


def log_intro(logger, dir_path, size_threshold, delete_files, log_file):
    """
    Log an introduction entry with relevant information.

    Args:
        logger (logging.Logger): Logger instance.
        dir_path (Path): Path to the target directory.
        size_threshold (Optional[int]): Size threshold for large files.
        delete_files (bool): Whether to delete reported files.
        log_file (Optional[str]): Path to the log file.
    """
    logger.info("File System Analysis - Starting Analysis")
    logger.info(f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Target Directory: {dir_path}")
    logger.info(f"Size Threshold for Large Files: {size_threshold} bytes")
    logger.info(f"Delete Files Flag: {delete_files}")
    logger.info(f"Log File: {log_file}")
    logger.info("=" * 50)


def process_directory(logger, dir_path, size_threshold, delete_files, log_file):
    """
    Process the target directory.

    Args:
        logger (logging.Logger): Logger instance.
        dir_path (Path): Path to the target directory.
        size_threshold (Optional[int]): Size threshold for large files.
        delete_files (bool): Whether to delete reported files.
        log_file (Optional[str]): Path to the log file.
    """
    file_categorization = FileCategorization()
    permissions_checker = FilePermissionsChecker()
    large_file_identifier = LargeFileIdentifier(size_threshold)

    for file_path in walk_through_dir(dir_path):
        file_categorization.add_file(file_path)
        permissions_checker.check_permissions(file_path)
        large_file_identifier.add_file(file_path)

    file_categorization.display_summary()
    permissions_checker.print_permission_report()

    if delete_files and permissions_checker.reported_files and not log_file:
        confirm = Confirm.ask("Do you want to delete the files with bad permissions?")
        if confirm:
            permissions_checker.delete_reported_files()

    large_file_identifier.scan_and_report()

    if delete_files and large_file_identifier.large_files and not log_file:
        confirm = Confirm.ask("Do you want to delete the large files?")
        if confirm:
            large_file_identifier.delete_reported_files()


def main():
    dir_path, size_threshold, delete_files, log_file = parse_args()
    if dir_path is None:
        exit(1)

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger()

    configure_log_file(log_file)
    log_intro(logger, dir_path, size_threshold, delete_files, log_file)
    process_directory(logger, dir_path, size_threshold, delete_files, log_file)


if __name__ == "__main__":
    main()
