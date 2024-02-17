import pytest

from analyzer.directory_traversal import walk_through_dir


@pytest.fixture
def test_directory(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "test_file_1.txt").write_text("content 1")
    (test_dir / "test_file_2.txt").write_text("content 2")
    sub_dir = test_dir / "sub_dir"
    sub_dir.mkdir()
    (sub_dir / "sub_file_1.txt").write_text("content 3")
    return test_dir


def test_walk_through_dir(test_directory, capsys):
    root_dir = test_directory
    files = list(walk_through_dir(root_dir))

    assert len(files) == 3

    expected_files = [
        root_dir / "test_file_1.txt",
        root_dir / "test_file_2.txt",
        root_dir / "sub_dir" / "sub_file_1.txt",
    ]

    for file in expected_files:
        assert file in files

    captured = capsys.readouterr()
    assert "Permission error" not in captured.out


def test_walk_through_empty_dir(tmp_path):
    empty_dir = tmp_path / "empty_dir"
    empty_dir.mkdir()

    files = list(walk_through_dir(empty_dir))
    assert len(files) == 0


def test_walk_through_dir_with_hidden_files(test_directory, capsys):
    root_dir = test_directory
    (root_dir / ".hidden_file").write_text("hidden content")

    files = list(walk_through_dir(root_dir))
    assert len(files) == 4

    expected_files = [
        root_dir / "test_file_1.txt",
        root_dir / "test_file_2.txt",
        root_dir / "sub_dir" / "sub_file_1.txt",
        root_dir / ".hidden_file",
    ]

    for file in expected_files:
        assert file in files

    captured = capsys.readouterr()
    assert "Permission error" not in captured.out


def test_walk_through_dir_with_symlink(tmp_path):
    root_dir = tmp_path / "root_dir"
    root_dir.mkdir()
    (root_dir / "file.txt").write_text("content")
    symlink_dir = tmp_path / "symlink_dir"
    symlink_dir.symlink_to(root_dir)

    files = list(walk_through_dir(symlink_dir))
    assert len(files) == 1

    expected_files = [symlink_dir / "file.txt"]

    for file in expected_files:
        assert file in files
