from pathlib import Path
from typing import Union


def walk_through_dir(root_dir: Union[str, Path]) -> None:
    """
    walk through the directory, subdirectories and files.

    Args:
        root_dir (Union[str, Path]): The root directory to start the traversal.

    Returns:
        None
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
