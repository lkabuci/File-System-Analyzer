from pathlib import Path
from typing import Dict, List, Union

import pytest
from bitmath import Byte, KiB, MiB
from pyfakefs.fake_filesystem import FakeFile, FakeFilesystem

# list of fake files to be created in the fake file system
fake_filesystem_files: List[Dict[str, Union[str, Byte, oct]]] = [
    {"name": "/root_dir/file_100_byte_0644.txt", "size": Byte(100), "perm": 0o644},
    {
        "name": "/root_dir/file_100_kb_0444.go",
        "size": KiB(100).to_Byte(),
        "perm": 0o444,
    },
    {
        "name": "/root_dir/file_100_kb_0444.pdf",
        "size": KiB(100).to_Byte(),
        "perm": 0o444,
    },
    {
        "name": "/root_dir/parent1/child1/file_10_mb_0755.rar",
        "size": MiB(10).to_Byte(),
        "perm": 0o755,
    },
    {
        "name": "/root_dir/parent1/child1/file_1_kb_0444.mp4",
        "size": KiB(1).to_Byte(),
        "perm": 0o444,
    },
    {
        "name": "/root_dir/parent1/child2/file_1_kb_0555.html",
        "size": KiB(1).to_Byte(),
        "perm": 0o555,
    },
    {
        "name": "/root_dir/parent1/file_10_mb_0755.txt",
        "size": MiB(10).to_Byte(),
        "perm": 0o755,
    },
    {
        "name": "/root_dir/parent2/child2/file_1_kb_0644.docx",
        "size": Byte(1024).to_Byte(),
        "perm": 0o644,
    },
    {
        "name": "/root_dir/parent2/child3/file_1_tb_0400.doc",
        "size": Byte(1024).to_Byte(),
        "perm": 0o400,
    },
    {
        "name": "/root_dir/parent2/child4/file_50_mb_0222.jpg",
        "size": MiB(50).to_Byte(),
        "perm": 0o222,
    },
    {
        "name": "/root_dir/parent2/child4/file_5_mb_0755.cpp",
        "size": MiB(5).to_Byte(),
        "perm": 0o755,
    },
    {
        "name": "/root_dir/parent2/child5/file_5_kb_0555.txt",
        "size": KiB(5).to_Byte(),
        "perm": 0o555,
    },
    {
        "name": "/root_dir/parent2/file_1_kb_0644.tar",
        "size": KiB(1).to_Byte(),
        "perm": 0o644,
    },
    {
        "name": "/root_dir/parent2/file_1_mb_0755.c",
        "size": MiB(1).to_Byte(),
        "perm": 0o755,
    },
    {
        "name": "/root_dir/parent2/file_200_byte_0755.py",
        "size": Byte(200),
        "perm": 0o755,
    },
    {
        "name": "/root_dir/parent2/file_500_byte_0600.json",
        "size": Byte(500),
        "perm": 0o600,
    },
    {
        "name": "/root_dir/parent2/file_512_kb_0444.mkv",
        "size": KiB(512).to_Byte(),
        "perm": 0o444,
    },
    {
        "name": "/root_dir/parent2/file_5_kb_0555.h",
        "size": KiB(5).to_Byte(),
        "perm": 0o555,
    },
    {
        "name": "/root_dir/parent3/child4/file_70_mb_0400.ogg",
        "size": MiB(70).to_Byte(),
        "perm": 0o400,
    },
    {
        "name": "/root_dir/parent3/file_600_byte_0700.py",
        "size": Byte(600),
        "perm": 0o700,
    },
    {
        "name": "/root_dir/parent4/child4/file_900_byte_0600.txt",
        "size": Byte(900),
        "perm": 0o600,
    },
    {
        "name": "/root_dir/parent5/child3/file_2_kb_0644.tar.gz",
        "size": KiB(2).to_Byte(),
        "perm": 0o644,
    },
    {
        "name": "/root_dir/parent5/child3/file_2_mb_0400.jpg",
        "size": MiB(2).to_Byte(),
        "perm": 0o400,
    },
    {
        "name": "/root_dir/parent5/child4/file_300_kb_0600.mp3",
        "size": KiB(300).to_Byte(),
        "perm": 0o600,
    },
    {
        "name": "/root_dir/parent5/child4/file_30_mb_0400.ogg",
        "size": MiB(30).to_Byte(),
        "perm": 0o400,
    },
    {
        "name": "/root_dir/parent5/child4/file_500_byte_0600.csv",
        "size": Byte(500),
        "perm": 0o600,
    },
    {
        "name": "/root_dir/parent5/file_20_mb_0222.png",
        "size": MiB(20).to_Byte(),
        "perm": 0o222,
    },
    {
        "name": "/root_dir/parent5/file_2_mb_0400.jpeg",
        "size": MiB(2).to_Byte(),
        "perm": 0o422,
    },
    {
        "name": "/root_dir/parent5/file_300_byte_0600.html",
        "size": Byte(300),
        "perm": 0o630,
    },
    {
        "name": "/root_dir/parent5/file_300_kb_0600.png",
        "size": KiB(300).to_Byte(),
        "perm": 0o603,
    },
]


def create_fakefs_file(
    fs: FakeFilesystem, filepath: str, mode: oct = 0o644, size: Byte = Byte(100)
) -> Path:
    """Create a fake file in the fake file system."""
    try:
        file: FakeFile = fs.create_file(
            file_path=filepath,
            st_mode=mode,
            contents="",
            st_size=int(size.value),
            create_missing_dirs=True,
            apply_umask=False,
            encoding=None,
            errors=None,
            side_effect=None,
        )
    except FileExistsError:
        pass
    return Path(file.path)


@pytest.fixture
def app_file_system(fs: FakeFilesystem):
    """Create a fake file system."""
    for file_info in fake_filesystem_files:
        create_fakefs_file(
            fs=fs,
            filepath=file_info["name"],
            mode=file_info["perm"],
            size=file_info["size"],
        )
    yield fs
    for file_info in fake_filesystem_files:
        fs.remove_object(file_info["name"])
