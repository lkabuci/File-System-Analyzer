import argparse
from pathlib import Path
from typing import Optional


def parse_args() -> Optional[Path]:
    """
    Parse command-line arguments.

    Returns:
        Path: Path to the target directory if it exists, None otherwise.
    """
    parser = argparse.ArgumentParser(
        description="Command-line tool that analyzes and reports on the file system structure and usage on a Linux system."
    )
    parser.add_argument("path", help="Path to the target directory")
    args = parser.parse_args()

    target_dir = Path(args.path)

    if not target_dir.exists():
        print("Error: The target directory doesn't exist.")
        return None

    return target_dir
