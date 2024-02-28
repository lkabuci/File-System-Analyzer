import argparse
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from rich import print

RED = "\033[91m"
RESET = "\033[0m"


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


def parse_args() -> (
    Optional[tuple[Path, Optional[int], bool, Optional[str], Optional[str]]]
):
    """
    Parse command-line arguments.

    Returns:
        Optional[tuple[Path, Optional[int], bool, Optional[str]]]: Tuple containing Path to the target directory,
        optional size parameter, delete flag, and optional log file.
    """
    parser = argparse.ArgumentParser(
        description="Command-line tool that analyzes and reports on the file"
        "system structure and usage on a Linux system."
    )
    parser.add_argument(
        "path",
        default=".",
        nargs="?",
        type=valid_path,
        help="Path to the target directory (default: current directory)",
    )
    parser.add_argument(
        "-s", "--size", type=int, help="Optional size threshold for large files"
    )
    parser.add_argument(
        "--size-unit",
        choices=["bytes", "KB", "MB", "GB"],
        default="bytes",
        help="Unit for displaying size in the summary table (default: bytes)",
    )
    parser.add_argument(
        "-d", "--delete", action="store_true", help="Enable file deletion prompt"
    )
    parser.add_argument("-l", "--log", type=str, help="Path to the log file")
    parser.add_argument(
        "-c", "--config", type=str, help="Path to the configuration file"
    )

    args = parser.parse_args()

    # Read configuration from file
    config = ConfigParser()
    if args.config:
        config.read(args.config)

    # Set default values or use values from the configuration file
    target_dir = Path(config.get("settings", "path", fallback=args.path))
    size_threshold = config.getint("settings", "size", fallback=args.size)
    delete_files = config.getboolean("settings", "delete", fallback=args.delete)
    log_file = config.get("settings", "log", fallback=args.log)

    target_dir.mkdir(parents=True, exist_ok=True)

    if not target_dir.is_dir():
        print("Error: The target path is not a directory.")
        return None

    return target_dir, size_threshold, delete_files, log_file, args.size_unit
