from analyzer.directory_traversal import walk_through_dir
from analyzer.file_categorization import FileCategorization
from analyzer.large_files_identification import LargeFileIdentifier
from analyzer.permission_reporter import FilePermissionsChecker
from analyzer.utils.parser import parse_args


def main():
    file_categorization = FileCategorization()
    permissions_checker = FilePermissionsChecker()
    large_file_identifier = LargeFileIdentifier()

    dir_path = parse_args()
    if dir_path is None:
        exit(1)

    for file_path in walk_through_dir(dir_path):
        file_categorization.add_file(file_path)
        permissions_checker.check_permissions(file_path)
        large_file_identifier.add_file(file_path)

    file_categorization.display_summary()
    permissions_checker.print_permission_report()
    large_file_identifier.scan_and_report()


if __name__ == "__main__":
    main()
