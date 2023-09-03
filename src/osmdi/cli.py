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

    # parser.add_argument(
    #     'integers', metavar='N', type=int, nargs='+',
    #     help='an integer for the accumulator')
    # parser.add_argument(
    #     '-greet', action='store_const', const=True,
    #     default=False, dest='greet',
    #     help="Greet Message from Geeks For Geeks.")
    # parser.add_argument(
    #     '--sum', dest='accumulate', action='store_const',
    #     const=sum, default=max,
    #     help='sum the integers (default: find the max)')

    # added --titles as aliases existing --page-title
    # parser.add_argument("--page-title", help="Page title of input")

    # parser_input = parser.add_argument_group(
    #     "input", "Input data. Select ONE of these options"
    # )

    # parser_input.add_argument(
    #     "--titles",
    #     "--page-title",
    #     help="MediaWiki page titles of input, Use | as separator",
    # )

    # # @TODO remove the rest
    # parser_input.add_argument(
    #     "--input-osmdi-compact",
    #     help="OSM data intent, compact input file",
    #     dest="in_compact",
    #     # action="store_true",
    # )

    # parser_input.add_argument(
    #     "--pageids", help="MediaWiki pageids of input, Use | as separator"
    # )

    # parser_input.add_argument(
    #     "--revids", help="MediaWiki revision IDs of input, Use | as separator"
    # )

    # Not fully implemented. Hidden at the moment
    # parser_input.add_argument(
    #     "--wikibase-ids",
    #     help="(Early draft) WikiBase Q items or P properties. Use | as separator",
    # )

    # parser_input.add_argument(
    #     "--input-autodetect",
    #     # action="store_true",
    #     help="Page titles, pageids (not both). "
    #     "Syntax sugar for --titles or --pageids. "
    #     "Use | as separator. (experimental) by category content fetch",
    # )

    # parser_input.add_argument(
    #     "--input-stdin",
    #     action="store_true",
    #     help="Use STDIN (data piped from other tools) instead of remote API",
    # )

    # parser_output = parser.add_argument_group(
    #     "output",
    #     "Output options.",
    # )

    # parser_output.add_argument(
    parser.add_argument(
        "-O",
        "--output-format",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format",
        dest="out_format",
    )

    # parser_output.add_argument(
    #     "--output-streaming",
    #     action="store_true",
    #     help="Output JSON Text Sequences (RFC 7464 application/json-seq)",
    # )

    # # parser.add_argument(
    # #     "--output-dir",
    # #     help="Output inferred files to a directory. "
    # #     "With --verbose will save input text and JSON-LD metadata",
    # # )

    # parser_output.add_argument(
    #     "--output-zip-stdout",
    #     action="store_true",
    #     help="Output inferred files to a zip (stdout)"
    #     "With --verbose will save input text and JSON-LD metadata",
    # )

    # parser_output.add_argument(
    #     "--output-zip-file",
    #     # action="store_true",
    #     help="Output inferred files to a zip (file)"
    #     "With --verbose will save input text and JSON-LD metadata",
    # )

    # parser_output.add_argument(
    #     "--output-file-by-name",
    #     dest="out_file_stdout",
    #     help="Filename hint for a single file be printed to stdout",
    # )

    # parser_output.add_argument(
    #     "--output-file-by-content",
    #     dest="out_filestr_stdout",
    #     help="(NOT IMPLEMNTED YET) Text content hint for a single file to be printed to stdout",
    # )

    # parser_output.add_argument(
    #     "--output-raw",
    #     action="store_true",
    #     help="[DEBUG] Output RAW, unedited Wiki markup (or API response if remote call)",
    # )

    # # parser_filter = parser.add_argument_group('filter2', 'Output data. Optional. Any of the following options will override the default JSON-LD to stdout option.')
    # parser_filter = parser.add_argument_group(
    #     "filter",
    #     "Filter data. Optional. Allow restrict only a subset of the items.",
    # )

    # parser_filter.add_argument(
    #     "--filter-item-type",
    #     # action="store_true",
    #     help="(experimental) Filter item @type values on JSON-LD. Python REGEX value",
    #     default=None,
    # )

    # parser_filter.add_argument(
    #     "--filter-item-id",
    #     # action="store_true",
    #     help="(experimental, not fully implememted) Filter item @id on JSON-LD. Python REGEX value",
    #     default=None,
    # )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose", dest="verbose"
    )

    args = parser.parse_args()

    # from .datafetch import DataFetch

    # df = DataFetch()
    # df.debug()
    # return EXIT_ERROR

    # print(args)

    # wikitext = None
    # wikiapi_meta = None

    # meta = {}

    # args.page_title = args.titles
    # print(args.page_title)

    # print("TODO")
    # osmdi = OsmDI(args.in_compact)
    osmdi = OsmDI(args.infile, output_format=args.out_format)
    osmdi.debug()
    return EXIT_OK
    # return EXIT_ERROR

    # if args.in_compact:
    #     # print("TODO")
    #     osmdi = OsmDI(args.in_compact)
    #     osmdi.debug(True)
    #     return EXIT_ERROR

    # print("TODO remove old code")

    return EXIT_ERROR


if __name__ == "__main__":
    main()


def exec_from_console_scripts():
    main()
