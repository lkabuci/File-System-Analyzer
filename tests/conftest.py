import os
from stat import ST_MODE

import pytest
from bitmath import Byte, KiB, MiB
from pyfakefs import fake_filesystem, fake_os

list_of_files = [
    {"name": "file_100_byte_0644.txt", "size": Byte(100), "perm": 0o644},
    {"name": "file_100_kb_0444.pdf", "size": KiB(100).to_Byte(), "perm": 0o444},
    {"name": "file_100_kb_0444.go", "size": KiB(100).to_Byte(), "perm": 0o444},
    {"name": "file_10_mb_0755.rar", "size": MiB(10).to_Byte(), "perm": 0o755},
    {"name": "file_10_mb_0755.txt", "size": MiB(10).to_Byte(), "perm": 0o755},
    {"name": "file_1_kb_0444.mp4", "size": KiB(1).to_Byte(), "perm": 0o444},
    {"name": "file_1_kb_0555.html", "size": KiB(1).to_Byte(), "perm": 0o555},
    {"name": "file_1_kb_0644.docx", "size": Byte(1024).to_Byte(), "perm": 0o644},
    {"name": "file_1_kb_0644.tar", "size": KiB(1).to_Byte(), "perm": 0o644},
    {"name": "file_1_mb_0755.c", "size": MiB(1).to_Byte(), "perm": 0o755},
    {"name": "file_1_tb_0400.doc", "size": Byte(1024).to_Byte(), "perm": 0o400},
    {"name": "file_200_byte_0755.py", "size": Byte(200), "perm": 0o755},
    {"name": "file_20_mb_0222.png", "size": MiB(20).to_Byte(), "perm": 0o222},
    {"name": "file_2_kb_0644.tar.gz", "size": KiB(2).to_Byte(), "perm": 0o644},
    {"name": "file_2_mb_0400.jpg", "size": MiB(2).to_Byte(), "perm": 0o400},
    {"name": "file_2_mb_0400.jpeg", "size": MiB(2).to_Byte(), "perm": 0o400},
    {"name": "file_300_byte_0600.html", "size": Byte(300), "perm": 0o600},
    {"name": "file_300_kb_0600.png", "size": KiB(300).to_Byte(), "perm": 0o600},
    {"name": "file_300_kb_0600.mp3", "size": KiB(300).to_Byte(), "perm": 0o600},
    {"name": "file_30_mb_0400.ogg", "size": MiB(30).to_Byte(), "perm": 0o400},
    {"name": "file_500_byte_0600.csv", "size": Byte(500), "perm": 0o600},
    {"name": "file_500_byte_0600.json", "size": Byte(500), "perm": 0o600},
    {"name": "file_50_mb_0222.jpg", "size": MiB(50).to_Byte(), "perm": 0o222},
    {"name": "file_512_kb_0444.mkv", "size": KiB(512).to_Byte(), "perm": 0o444},
    {"name": "file_5_kb_0555.txt", "size": KiB(5).to_Byte(), "perm": 0o555},
    {"name": "file_5_kb_0555.h", "size": KiB(5).to_Byte(), "perm": 0o555},
    {"name": "file_5_mb_0755.cpp", "size": MiB(5).to_Byte(), "perm": 0o755},
    {"name": "file_600_byte_0700.py", "size": Byte(600), "perm": 0o700},
    {"name": "file_70_mb_0400.ogg", "size": MiB(70).to_Byte(), "perm": 0o400},
    {"name": "file_900_byte_0600.txt", "size": Byte(900), "perm": 0o600},
]

# Reduce the size of MiB files by 10%
for file_info in list_of_files:
    if isinstance(file_info["size"], MiB):
        file_info["size"] = file_info["size"] * 0.9


def create_file(
    filesystem,
    os_module: fake_os.FakeOsModule,
    pathname: str,
    size: Byte = Byte(100),
    permissions: int = 0o644,
):
    """Create a file with the specified size and permissions."""
    filesystem.create_file(pathname)
    fd = os_module.open(pathname, os.O_WRONLY | os.O_CREAT, 0o644)
    os_module.write(fd, b"\0" * int(size.value))
    os_module.close(fd)
    os_module.chmod(pathname, permissions)


@pytest.fixture(scope="session")
def analyze_file_permissions():
    filesystem = fake_filesystem.FakeFilesystem()
    os_module = fake_os.FakeOsModule(filesystem)
    for file_info in list_of_files:
        print("\n", file_info["name"], end=", ")
        print(file_info["size"], end=", ")
        print(file_info["perm"], end="\n")
        create_file(
            filesystem,
            os_module,
            file_info["name"],
            file_info["size"],
            file_info["perm"],
        )
    yield filesystem, os_module
    for file_info in list_of_files:
        filesystem.remove_object(file_info["name"])
    del filesystem, os_module
