import itertools

from typing import Iterable, List

import pandas as pd


def pandas_print_full(x: pd.DataFrame):
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 2000)
    pd.set_option("display.float_format", "{:20,.2f}".format)
    pd.set_option("display.max_colwidth", None)
    print(x)
    pd.reset_option("display.max_rows")
    pd.reset_option("display.max_columns")
    pd.reset_option("display.width")
    pd.reset_option("display.float_format")
    pd.reset_option("display.max_colwidth")


def slug_to_url(slug: str) -> str:
    return f"https://opensea.io/collection/{slug}"


def consume_first(gen: Iterable) -> List:
    return list(itertools.islice(gen, 1))
