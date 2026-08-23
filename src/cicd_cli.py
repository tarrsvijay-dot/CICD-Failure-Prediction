import argparse

from src.cicd_check import check


def main():

    parser = argparse.ArgumentParser(
        prog="cicd",
        description="CI/CD pipeline analysis and failure prediction tool"
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Analyze the current Git repository"
    )

    args = parser.parse_args()

    if args.check:
        check()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()