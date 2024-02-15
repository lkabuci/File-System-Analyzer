from analyzer.directory_traversal import walk_through_dir
from analyzer.file_categorization import FileCategorization
from analyzer.parser.parser import parse_args
from analyzer.permission_reporter import FilePermissionsChecker


def main():
    fileC = FileCategorization()
    permission_reportter = FilePermissionsChecker()
    dir_path = parse_args()
    if dir_path is None:
        SystemExit(1)

    for file in walk_through_dir(dir_path):
        fileC.add_file(file)
        permission_reportter.check_permissions(file)

    fileC.display_summary()
    permission_reportter.report_permissions()


if __name__ == "__main__":
    main()
