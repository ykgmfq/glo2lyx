"""
Replaces glossary keywords in LyX text with `nomenclature` commands.
With `nomenclature` renewed as `gls`, these render as glossary entries.
"""

from pathlib import Path
import csv
import string
import argparse
import logging
import sys
import pprint


def cmdline() -> argparse.Namespace:
    """
    CLI setup
    """
    parser = argparse.ArgumentParser(
        prog="glo2lyx",
        description="Convert plain-text glossary keys in your LyX files to LyX commands.",
        epilog="The Lyx files must be stored in plain text. See the README for configuration guidance.",
    )
    parser.add_argument(
        "glossary", type=Path, help="a tex file with abbreviation definitions"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=True,
        help="search recursively for LyX files, defaults to true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "dir",
        nargs="?",
        type=Path,
        default=Path(),
        help="the directory containing your LyX files, defaults to working directory",
    )

    return parser.parse_args()


def get_keys(source: Path) -> list[str]:
    """
    Searches the source file for `\\newabbreviation{}` commands.
    The first argument becomes the key.
    """
    # Get newabbreviation entries
    if source.suffix != ".tex":
        logging.warning("Keys file is not a TeX file.")
    with open(source) as file:
        rows = csv.reader(file, delimiter="{")
        # Get first argument, stip trailing curly bracket.
        keys = [row[1][:-1] for row in rows if "\\newabbreviation" in row[:1]]
    logging.info(f"Parsed these keys: {pprint.pformat(keys,compact=True)}")
    return keys


def convert(keys: list[str], lyxdir: Path, recursive: bool = True):
    """
    The keys are used with the template to create `nomenclature` commands.
    """
    # Setup
    templ = string.Template(r"""
\begin_inset CommandInset nomenclature
LatexCommand nomenclature
symbol "$key"
description "a"
literal "false"
\end_inset

""")
    files = lyxdir.rglob("*.lyx") if recursive else lyxdir.glob("*.lyx")
    empty = True
    # Replace
    for lyxfile in files:
        text = lyxfile.read_text()
        for key in keys:
            nomencl = templ.substitute(key=key)
            text = text.replace(f" {key} ", f" {nomencl} ")
            text = text.replace(f"#{key}", nomencl)
        lyxfile.write_text(text)
        logging.info(f"Processed {str(lyxfile.resolve())}")
        empty = False
    if empty:
        logging.warning(f"No Lyx files found at {str(lyxdir.resolve())}")


def main():
    args = cmdline()
    logging.basicConfig(format="%(levelname)s: %(message)s")
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    keys = get_keys(args.glossary)
    if len(keys) == 0:
        logging.error(f"No keys found in {str(args.glossary.resolve())}")
        sys.exit(2)
    convert(keys, args.dir, args.recursive)


if __name__ == "__main__":
    main()
