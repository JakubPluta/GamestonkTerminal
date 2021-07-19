"""DeFi Rate View"""
__docformat__ = "numpy"

import argparse
from typing import List
import pandas as pd
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup
from gamestonk_terminal.helper_funcs import (
    parse_known_args_and_warn,
)


def replace_pct(x):
    if x == "–":
        return ""
    if x.endswith("%"):
        x = x.replace("%", "")
        return float(x)
    return x


def choose_current_or_last_30days(soup, current=True):
    if current:
        print("Displaying current values", "\n")
        return soup.find("div", class_="table-container").find("table")
    print("Displaying 30 day average values", "\n")
    return soup.find("div", class_="table-container table-hidden").find("table")


def get_funding_rates(other_args: List[str]):
    """Funding rates are transfer payments made between long and short positions on perpetual swap futures markets.
    They’re designed to keep contract prices consistent with the underlying asset.

    Parameters
    ----------
    other_args: List[str]
        Arguments to pass to argparse
    """

    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="funding",
        description="""
        Funding rates influence the price of perpetual swap contracts by penalizing or rewarding traders,
        depending on the nature of their position (long or short). The side of the market benefitting from the funding
        rate is determined by the difference between the contract price and the price of the underlying asset.
        When the contract price is too high – defined as being above spot price - long positions will pay
        short positions a fee.Conversely, when the contract price is too low – defined as being below spot price
        short positions will pay long positions a fee.
        [Source:  https://defirate.com/funding/]""",
    )
    parser.add_argument(
        "--current",
        action="store_false",
        default=True,
        dest="current",
        help="Show Current Funding Rates or Last 30 Days Average",
    )

    try:
        ns_parser = parse_known_args_and_warn(parser, other_args)

        if not ns_parser:
            return

        url = "https://defirate.com/funding/"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, features="lxml")
        table = choose_current_or_last_30days(soup, ns_parser.current)
        items = []
        first_row = table.find("thead").text.strip().split()
        headers = [r for r in first_row if r != "Trade"]
        headers.insert(0, "Symbol")
        for i in table.find_all("td"):
            items.append(i.text.strip())
        fundings = [items[i : i + 5] for i in range(0, len(items), 5)]
        df = pd.DataFrame(columns=headers, data=fundings)

        if df.empty:
            print("No data found", "\n")
            return

        print("")
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".5f",
                showindex=False,
                tablefmt="fancy_grid",
            )
        )
        print("")

    except Exception as e:
        print(e, "\n")


def lending(other_args: List[str]):
    """
    Decentralized Finance lending – or DeFi lending for short – allows users to supply cryptocurrencies
    in exchange for earning an annualized return

    Parameters
    ----------
    other_args: List[str]
        Arguments to pass to argparse
    """

    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="lending",
        description="""
        Decentralized Finance lending – or DeFi lending for short – allows users to supply cryptocurrencies
        in exchange for earning an annualized return
        [Source:  https://defirate.com/lend/]""",
    )
    parser.add_argument(
        "--current",
        action="store_false",
        default=True,
        dest="current",
        help="Show Current Lending Rates or Last 30 Days Average",
    )

    try:
        ns_parser = parse_known_args_and_warn(parser, other_args)

        if not ns_parser:
            return

        url = "https://defirate.com/loans/?exchange_table_type=lend"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, features="lxml")
        table = choose_current_or_last_30days(soup, ns_parser.current)
        items = []
        first_row = table.find("thead").text.strip().split("\n")

        headers = [r for r in first_row if r not in ["Lend", ""]]
        headers.insert(0, "Symbol")
        for i in table.find_all("td"):
            items.append(i.text.strip())
        lendings = [items[i : i + 12] for i in range(0, len(items), 12)]
        df = pd.DataFrame(columns=headers, data=lendings)

        if df.empty:
            print("No data found", "\n")
            return

        print("")
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".5f",
                showindex=False,
                tablefmt="fancy_grid",
            )
        )
        print("")

    except Exception as e:
        print(e, "\n")


def borrow(other_args: List[str]):
    """
    Perhaps one of the most exciting aspects of Decentralized Finance (DeFi) is the ability to take out a loan on
    top cryptocurrencies at any time in an entirely permissionless fashion.
    By using smart contracts, borrowers are able to lock collateral to protect against defaults while seamlessly
    adding to or closing their loans at any time.

    Parameters
    ----------
    other_args: List[str]
        Arguments to pass to argparse
    """

    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="borrow",
        description="""
        Perhaps one of the most exciting aspects of Decentralized Finance (DeFi) is the ability to take out a
        loan on top cryptocurrencies at any time in an entirely permissionless fashion.
        By using smart contracts, borrowers are able to lock collateral to protect against defaults while seamlessly
        adding to or closing their loans at any time.
        [Source:  https://defirate.com/loans/]""",
    )
    parser.add_argument(
        "--current",
        action="store_false",
        default=True,
        dest="current",
        help="Show Current Borrow Rates or Last 30 Days Average",
    )

    try:
        ns_parser = parse_known_args_and_warn(parser, other_args)

        if not ns_parser:
            return

        url = "https://defirate.com/loans/?exchange_table_type=borrow"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, features="lxml")
        table = choose_current_or_last_30days(soup, ns_parser.current)
        items = []
        first_row = table.find("thead").text.strip().split("\n")

        headers = [r for r in first_row if r not in ["Borrow", ""]]
        headers.insert(0, "Symbol")
        for i in table.find_all("td"):
            items.append(i.text.strip())
        borrowings = [items[i : i + 12] for i in range(0, len(items), 12)]
        df = pd.DataFrame(columns=headers, data=borrowings)

        if df.empty:
            print("No data found", "\n")
            return

        print("")
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".5f",
                showindex=False,
                tablefmt="fancy_grid",
            )
        )
        print("")

    except Exception as e:
        print(e, "\n")
