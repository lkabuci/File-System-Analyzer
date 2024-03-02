from analyzer.file_processing import process_directory
from analyzer.utils.logger import setup_logging
from analyzer.utils.parser import parse_args


def main():
    arguments = parse_args()
    if arguments.target_dir is None:
        exit(1)

    setup_logging(
        log_file=arguments.log_file,
        target_dir=arguments.target_dir,
        size_threshold=arguments.size_threshold,
        delete_files=arguments.delete_files,
    )

    process_directory(
        dir_path=arguments.target_dir,
        size_threshold=str(arguments.size_threshold),
        delete_files=arguments.delete_files,
        log_file=arguments.log_file,
    )


if __name__ == "__main__":
    main()
