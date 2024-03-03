import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel


class LogInfo(BaseModel):
    """
    Data model for log information.

    Attributes:
        target_dir (Optional[Union[Path, str]]): Path to the target directory.
        size_threshold (Optional[str]): Size threshold for large files.
        delete_files (Optional[bool]): Whether to delete reported files.
        log_file (Optional[str]): Path to the log file.
    """

    target_dir: Optional[Union[Path, str]]
    size_threshold: Optional[str]
    delete_files: Optional[bool]
    log_file: Optional[str]


def configure_log_file(log_file):
    """
    Configure log file redirection if provided.
    """
    if log_file:
        sys.stdout = open(file=log_file, mode="a", encoding="utf-8")
        sys.stderr = open(file=log_file, mode="a", encoding="utf-8")


def log_intro(loginfo: LogInfo):
    """
    Log the introduction to the analysis.

    Args:
        loginfo (LogInfo): Log information.
    """

    logger = logging.getLogger()
    logger.info("File System Analysis - Starting Analysis")
    logger.info("Date and Time: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("Target Directory: %s", loginfo.target_dir)
    logger.info("Size Threshold for Large Files: %s bytes", loginfo.size_threshold)
    logger.info("Delete Files Flag: %s", loginfo.delete_files)
    logger.info("Log File: %s", loginfo.log_file)
    logger.info("=" * 50)


def setup_logging(
    log_file: Optional[str], target_dir: Path, size_threshold: str, delete_files: bool
) -> None:
    """
    Set up logging configuration.

    Args:
        log_file (Optional[str]): Path to the log file (optional).
        target_dir (Path): Path to the target directory.
        size_threshold (str): Size threshold for identifying large files.
        delete_files (bool): Flag indicating whether file deletion prompt is enabled.

    Returns:
        None
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    configure_log_file(log_file)
    log_intro(
        LogInfo(
            target_dir=target_dir,
            size_threshold=size_threshold,
            delete_files=delete_files,
            log_file=log_file,
        )
    )
