from pathlib import Path

from analyzer.directory_traversal import walk_through_dir
from analyzer.file_categorization import FileCategorization
from analyzer.parser.parser import parse_args
from analyzer.permission_reporter import FilePermissionsChecker


def main():
    file_categorization = FileCategorization()
    permissions_checker = FilePermissionsChecker()

    dir_path = parse_args()
    if dir_path is None:
        exit(1)

    for file_path in walk_through_dir(dir_path):
        file_categorization.add_file(file_path)
        permissions_checker.check_permissions(file_path)

    file_categorization.display_summary()
    permissions_checker.print_permission_report()


if __name__ == "__main__":
    main()
