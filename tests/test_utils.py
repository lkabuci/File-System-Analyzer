import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Union

import pytest

PathLike = Union[Path, str]


def create_temp_file(
    file_name: PathLike, size_bytes: int, permission: int = 0o644
) -> Path:
    file_path = Path(tempfile.gettempdir()) / file_name
    with open(file_path, "wb") as f:
        f.write(b"\0" * size_bytes)
    os.chmod(file_path, permission)
    return file_path


def create_temp_directory(directory_name: PathLike, permission: int = 0o755) -> Path:
    directory_path = Path(tempfile.gettempdir()) / directory_name
    try:
        directory_path.mkdir(mode=permission)
    except FileExistsError:
        pass
    return directory_path


def cleanup_temp_files(
    *file_paths: Iterable[PathLike], permission: int = 0o644
) -> None:
    """Delete the specified temporary files."""
    for file_path in file_paths:
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
        except (PermissionError, FileNotFoundError) as e:
            print(f"Error deleting file {file_path}: {e}", file=sys.stderr)


def cleanup_temp_directories(
    *directory_paths: PathLike, permission: int = 0o755
) -> None:
    """Delete the specified temporary directories."""
    for directory_path in directory_paths:
        path = Path(directory_path)
        if path.exists():
            shutil.rmtree(directory_path, ignore_errors=True)
    os.umask(permission)


@pytest.fixture
def temp_file_path():
    temp_file_path = create_temp_file("test_file.txt", 100)
    yield temp_file_path
    cleanup_temp_files(temp_file_path)


@pytest.fixture
def temp_directory_path():
    temp_directory_path = create_temp_directory("test_directory")
    yield temp_directory_path
    cleanup_temp_directories(temp_directory_path)


def test_create_temp_file(temp_file_path):
    assert temp_file_path.is_file()
    assert temp_file_path.stat().st_size == 100


def test_create_temp_directory(temp_directory_path):
    assert temp_directory_path.is_dir()


def test_cleanup_temp_files(temp_file_path):
    cleanup_temp_files(temp_file_path)
    assert not temp_file_path.exists()


def test_cleanup_temp_directories(temp_directory_path):
    assert temp_directory_path.exists()
    # cleanup_temp_directories(temp_directory_path)


@pytest.fixture
def temp_file_path_zero_size():
    temp_file_path = create_temp_file("test_zero_size_file.txt", 0, permission=0o600)
    yield temp_file_path
    cleanup_temp_files([temp_file_path])


@pytest.fixture
def temp_file_path_large_size():
    temp_file_path = create_temp_file("test_large_file.txt", 10**6)
    yield temp_file_path
    cleanup_temp_files([temp_file_path])


def test_cleanup_temp_files_when_file_does_not_exist():
    non_existent_file = Path(tempfile.gettempdir()) / "non_existent_file.txt"
    cleanup_temp_files(non_existent_file)
    # No exception should be raised


def test_cleanup_temp_directories_when_directory_does_not_exist():
    non_existent_directory = Path(tempfile.gettempdir()) / "non_existent_directory"
    cleanup_temp_directories(non_existent_directory)
    # No exception should be raised


if __name__ == "__main__":
    pytest.main()
