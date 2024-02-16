import argparse
from pathlib import Path
from typing import Optional


def parse_args() -> Optional[tuple[Path, Optional[int]]]:
    """
    Parse command-line arguments.

    Returns:
        Optional[tuple[Path, Optional[int]]]: Tuple containing Path to the target directory
        and optional size parameter.
    """
    parser = argparse.ArgumentParser(
        description="Command-line tool that analyzes and reports on the file system structure and usage on a Linux system."
    )
    parser.add_argument("path", help="Path to the target directory")
    parser.add_argument(
        "-s", "--size", type=int, help="Optional size threshold for large files"
    )

    args = parser.parse_args()

    target_dir = Path(args.path)

    if not target_dir.exists():
        print("Error: The target directory doesn't exist.")
        return None

    return target_dir, args.size
