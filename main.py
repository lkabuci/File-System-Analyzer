from analyzer.directory_traversal import walk_through_dir
from analyzer.parser.parser import parse_args


def main():
    dir_path = parse_args()
    if dir_path is None:
        SystemExit(1)
    walk_through_dir(dir_path)


if __name__ == "__main__":
    main()
