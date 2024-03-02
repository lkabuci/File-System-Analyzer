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
        sys.stdout = open(log_file, "a")
        sys.stderr = open(log_file, "a")


def log_intro(loginfo: LogInfo):
    """
    Log the introduction to the analysis.

    Args:
        loginfo (LogInfo): Log information.
    """

    logger = logging.getLogger()
    logger.info("File System Analysis - Starting Analysis")
    logger.info(f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Target Directory: {loginfo.target_dir}")
    logger.info(f"Size Threshold for Large Files: {loginfo.size_threshold} bytes")
    logger.info(f"Delete Files Flag: {loginfo.delete_files}")
    logger.info(f"Log File: {loginfo.log_file}")
    logger.info("=" * 50)


def setup_logging(log_file, target_dir, size_threshold, delete_files):
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
