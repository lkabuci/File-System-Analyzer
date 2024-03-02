import argparse
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

import bitmath
from pydantic import BaseModel, Field
from rich import print

RED = "\033[91m"
RESET = "\033[0m"


class ParsedArgs(BaseModel):
    """
    Data model for parsed command-line arguments.

    Attributes:
        target_dir (Path): Path to the target directory.
        size_threshold (int): Size threshold for identifying large files.
        delete_files (bool): Flag indicating whether file deletion prompt is enabled.
        log_file (Optional[str]): Path to the log file (optional).
    """

    target_dir: Path
    size_threshold: str
    delete_files: bool
    log_file: Optional[str]


def valid_path(path: str) -> Path:
    """
    Validate the path provided as a command-line argument.

    Args:
        path (str): The path to be validated.

    Returns:
        Path: The validated path as a Path object.
    """
    path = Path(path)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"{RED}Invalid path: {path}{RESET}")
    return path


def parse_args() -> Optional[ParsedArgs]:
    """
    Parse command-line arguments.

    Returns:
        Optional[ParsedArgs]: Parsed command-line arguments as an instance of ParsedArgs.
    """
    parser = argparse.ArgumentParser(
        description="Command-line tool that analyzes and reports on the filesystem structure and usage on a Linux system."
    )

    parser.add_argument(
        "path",
        default=".",
        nargs="?",
        type=valid_path,
        help="Path to the target directory (default: current directory)",
    )

    parser.add_argument(
        "-s",
        "--size",
        type=bitmath.parse_string,
        default=bitmath.parse_string("1 MiB"),
        help="Size threshold for identifying large files. "
        "Enter a number followed by the unit type, e.g., 100 MB. "
        f"Valid unit types: {bitmath.ALL_UNIT_TYPES} (default: 1 MiB)",
    )

    parser.add_argument(
        "-d", "--delete", action="store_true", help="Enable file deletion prompt"
    )

    parser.add_argument(
        "-l", "--log", type=valid_path, default=None, help="Path to the log file"
    )

    parser.add_argument(
        "-c", "--config", type=valid_path, help="Path to the configuration file"
    )

    args = parser.parse_args()

    # Read configuration from file
    config = ConfigParser()
    if args.config:
        config.read(args.config)

    # Set default values or use values from the configuration file
    target_dir = Path(config.get("settings", "path", fallback=args.path))
    size_threshold = config.get("settings", "size", fallback=args.size)
    delete_files = config.getboolean("settings", "delete", fallback=args.delete)
    log_file = config.get("settings", "log", fallback=args.log)

    return ParsedArgs(
        target_dir=target_dir,
        size_threshold=str(size_threshold),
        delete_files=delete_files,
        log_file=log_file,
    )
