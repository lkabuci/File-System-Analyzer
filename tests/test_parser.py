import argparse
from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from analyzer.utils.parser import valid_path


def test_valid_path_existing_file(fs: FakeFilesystem):
    fs.create_file("/test.txt")
    path = valid_path("/test.txt")
    assert isinstance(path, Path)
    assert path == Path("/test.txt")


def test_valid_path_existing_directory(fs: FakeFilesystem):
    fs.create_dir("/test_dir")
    path = valid_path("/test_dir")
    assert isinstance(path, Path)
    assert path == Path("/test_dir")


def test_valid_path_non_existing_path(fs: FakeFilesystem):
    with pytest.raises(argparse.ArgumentTypeError):
        valid_path("/non_existing_path")


def test_valid_path_with_relative_path(fs: FakeFilesystem):
    fs.create_file("/test.txt")
    path = valid_path("test.txt")
    assert isinstance(path, Path)
    assert path == Path("test.txt")
