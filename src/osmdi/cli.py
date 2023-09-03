import argparse
import json
import os
import sys
import osmdi
from osmdi.osmdi import OsmDI

# from osmdi.osmdi import WikiAsBase2Zip

EXIT_OK = 0  # pylint: disable=invalid-name
EXIT_ERROR = 1  # pylint: disable=invalid-name
EXIT_SYNTAX = 2  # pylint: disable=invalid-name


# Local install of cli (without upload).
#   python3 -m build
#   python3 -m pip install dist/osmdi-0.2.1-py3-none-any.whl --force

# Examples
#   osmdi --page-title 'User:EmericusPetro/sandbox/Wiki-as-base' | jq .data[1].data_raw
#   osmdi --input-stdin < tests/data/multiple.wiki.txt | jq .data[1].data_raw
#   cat tests/data/multiple.wiki.txt | osmdi --input-stdin | jq .data[1].data_raw


def main():
    parser = argparse.ArgumentParser(
        prog="osmdi",
        description="openstreetmap-data-intent proof of concept",
    )

    parser.add_argument(
        "infile",
        help="Osmdi file (if omitted, use standard input). Use - for stdin",
        nargs="?",
    )

    parser.add_argument(
        "-O",
        "--output-format",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format",
        dest="out_format",
    )

    # parser.add_argument(
    #     "-v", "--verbose", action="store_true", help="Verbose", dest="verbose"
    # )

    args = parser.parse_args()

    osmdi = OsmDI(args.infile, output_format=args.out_format)
    osmdi.debug()
    return EXIT_OK


#  return EXIT_ERROR


if __name__ == "__main__":
    main()


def exec_from_console_scripts():
    main()
