import sys

from analyzer.file_processing import process_directory
from analyzer.utils.logger import setup_logging
from analyzer.utils.parser import parse_args


def main():
    arguments = parse_args()
    if not arguments or not arguments.target_dir:
        sys.exit(1)

    setup_logging(
        log_file=arguments.log_file,
        target_dir=arguments.target_dir,
        size_threshold=arguments.size_threshold,
        delete_files=arguments.delete_files,
    )

    try:
        process_directory(
            dir_path=arguments.target_dir,
            size_threshold=str(arguments.size_threshold),
            delete_files=arguments.delete_files,
            log_file=arguments.log_file,
        )
    finally:
        if arguments.log_file is not None:

            # Close log file
            sys.stdout.close()
            sys.stderr.close()

            # Reset back to stanrds
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__


if __name__ == "__main__":
    main()
