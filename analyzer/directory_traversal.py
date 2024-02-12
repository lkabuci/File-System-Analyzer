from pathlib import Path
from typing import Union


def walk_through_dir(root_dir: Union[str, Path]) -> None:
    """
    Recursively walk through the directory and print subdirectories and files.

    Args:
        root_dir (Union[str, Path]): The root directory to start the traversal.

    Returns:
        None
    """
    root_path = Path(root_dir)

    for child in root_path.iterdir():
        if child.is_dir():
            print(f"Subdirectory: {child}")
            try:
                walk_through_dir(child)  # Recursively call for subdirectories
            except PermissionError as e:
                print(f"Permission error accessing directory: {child} {e}. Skipping...")
        else:
            try:
                print(f"File: {child}")
                # Add your file processing logic here
            except PermissionError as e:
                print(f"Permission error accessing file: {child} {e}. Skipping...")
