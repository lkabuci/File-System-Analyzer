from pathlib import Path
from typing import Generator, Union


def walk_through_dir(root_dir: Union[str, Path]) -> Generator[Path, None, None]:
    """
    Walk through the directory, subdirectories, and files.

    Args:
        root_dir (Union[str, Path]): The root directory to start the traversal.

    Yields:
        Generator[Path, None, None]: Yields FileInfo objects for each file in the directory tree.
    """
    root_path = Path(root_dir)
    stack = [root_path]

    while stack:
        current_path = stack.pop()

        for child in current_path.iterdir():
            if child.is_dir():
                stack.append(child)
            else:
                try:
                    yield child
                except PermissionError as e:
                    print(f"Permission error accessing file: {child} {e}. Skipping...")
