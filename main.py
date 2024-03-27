# pylint: disable=missing-docstring
import platform
import sys

from rich import print as pr

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


def is_valid_environment() -> bool:
    if platform.system() != "Linux":
        pr("[bold red]Error:[/] This tool is designed to run on Linux systems only.")
        pr("[bold red]Please run this script on a Linux system to proceed.[/]")
        return False

    if platform.python_version_tuple()[0] < "3":
        pr("[bold red]Error:[/] This tool is designed to run on Python 3.")
        pr("[bold red]Please use Python 3 to run this script.[/]")
        return False

    return True


if __name__ == "__main__":
    if not is_valid_environment():
        sys.exit(1)

    main()
