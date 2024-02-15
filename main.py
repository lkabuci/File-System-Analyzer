from analyzer.parser.parser import parse_args
from analyzer.directory_traversal import walk_through_dir

from analyzer.file_categorization import FileCategorization

def main():
    fileC = FileCategorization()
    dir_path = parse_args()
    if dir_path is None:
        SystemExit(1)

    for file in walk_through_dir(dir_path):
        fileC.add_file(file)

    fileC.display_summary()

if __name__ == "__main__":
    main()
