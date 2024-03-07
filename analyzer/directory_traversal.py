import sys
from pathlib import Path
from typing import Generator, List, Union

import rich


def walk_through_dir(root_dir: Union[str, Path]) -> Generator[Path, None, None]:
    """
    Walk through the directory, subdirectories, and files.

    Args:
        root_dir (Union[str, Path]): The root directory to start the traversal.

    Yields:
        Generator[Path, None, None]: Yields Path objects for each file
        in the directory tree.
    """
    root_path = Path(root_dir)
    stack: List[Path] = [root_path]

    while stack:
        current_path = stack.pop()
        yield from process_path(stack, current_path)


def process_path(stack: List[Path], current_path: Path) -> Generator[Path, None, None]:
    """
    Process a given path, yielding files and handling directories.

    Args:
        stack (List[Path]): The stack used for directory traversal.
        current_path (Path): The path to process.

    Yields:
        Generator[Path, None, None]: Yields Path objects for each file
        in the processed path.
    """
    try:
        for child in current_path.iterdir():
            if child.is_dir():
                stack.append(child)
            else:
                yield child
    except PermissionError:
        handle_permission_error(current_path)


def handle_permission_error(current_path: Path) -> None:
    """
    Handle PermissionError when accessing a directory.

    Args:
        current_path (Path): The path where the PermissionError occurred.
    """
    rich.print(
        f"[red]Permission error accessing directory '{current_path}'"
        ". Skipping...[/red]",
        file=sys.stderr,
    )
